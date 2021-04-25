from app import db
from app.database.champions import Champion
from flask_appbuilder.models.sqla.interface import SQLAInterface


def create_champion_model():
    return ChampionModel(Champion, db.session)


class ChampionModel(SQLAInterface):
    origin_datamodel = create_origin_model()
    classes_datamodel = create_classes_model()

    def clone(self, item: Hardware):
        new_item = self._copy(item)
        self.add(new_item)

    @staticmethod
    def _copy(item: Hardware):
        new_item = Hardware(
            device_id=item.device_id,
            template_id=item.template_id,
            serial_number=item.serial_number,
            asset_tag=item.asset_tag,
            info=item.info,
        )
        return new_item

    def csv_header(self):
        csv_columns = [
            "device",
            "template",
            "serial_number",
            "asset_tag",
            "info",
        ]
        return csv_columns

    @staticmethod
    def export_items(items):
        data = {"hardware": [], "device": []}
        for item in items:
            if not item:
                continue
            hardware_data = item.to_json()
            hardware_data["device"] = item.device.name if item.device_id else None
            hardware_data["template"] = item.template.name if item.template_id else None
            data["hardware"].append(hardware_data)

            device_data = item.device.to_json()
            device_list = data.get("device")
            if device_list:
                check = True
                for device in device_list:
                    if device.get("name") == device_data.get("name"):
                        check = False
                        template_data = item.template.to_json()
                        template_data["device"] = (
                            item.template.device.name if item.template_id else None
                        )
                        template_list = device.get("template")
                        if template_data not in template_list:
                            device["template"].append(template_data)
                if check:
                    template_data = item.template.to_json()
                    template_data["device"] = (
                        item.template.device.name if item.template_id else None
                    )
                    device_data["template"] = [template_data]
                    data["device"].append(device_data)

            else:
                template_data = item.template.to_json()
                template_data["device"] = (
                    item.template.device.name if item.template_id else None
                )
                device_data["template"] = [template_data]
                data["device"].append(device_data)

            # mac_lists = self.get_mac_addresses(item.id)
            # if mac_lists:
            #     mac_data = self.mac_datamodel.export_items(mac_lists)
            #     hardware_data.update(mac_data)
        return data

    def export_csv(self, items: list):
        data = self.export_items(items)
        hardware_data = data.get("hardware")
        if hardware_data:
            csv_columns = items[0].get_fields()
            csv_columns.remove("id")
            csv_columns.remove("device_id")
            csv_columns.remove("template_id")
            for hardware in hardware_data:
                del hardware["id"]
                del hardware["device_id"]
                del hardware["template_id"]
            outfile = write_csv(data=hardware_data, csv_columns=csv_columns)
            filename = f"Hardware-Export.csv"
            return outfile, filename
        else:
            return None, None

    def export_json(self, items: list):
        data = {"name": "hardware", "version": appversion()}
        hardware_data = self.export_items(items)
        data.update(hardware_data)
        outfile = write_json(data)
        filename = f"Hardware-Export.json"
        return outfile, filename

    def import_data(self, data=None):
        pk = -1
        if data:
            length = len(data)
            for hardware in data:
                if hardware.get("device") is None:
                    flash(
                        f"ERROR - Hardware device missing device", "error",
                    )
                elif hardware.get("template") is None:
                    flash(
                        f"ERROR - Hardware device missing template", "error",
                    )
                else:
                    new_hardware = Hardware.from_dict(hardware)
                    new_hardware.device_id = Device.get_by_name(
                        hardware.get("device")
                    ).id
                    new_hardware.template_id = TemplateModel.get_id(hardware.get("template"))
                    self.add(new_hardware)
                    if length == 1:
                        pk = new_hardware.id
                    # mac_data = hardware.get("mac_address")
                    # if mac_data:
                    #     self.mac_datamodel.import_data_hardware(
                    #         data=hardware,
                    #         hardware_id=new_hardware.id,
                    #     )
                    # flash(
                    #     f"Hardware device {new_hardware.device.name}-{new_hardware.serial_number} was added ",
                    #     "success",
                    # )
        else:
            flash("No new hardware were added", "warning")
        return pk

    # TODO check logic at the self.import_data level, having data type issues trying to match with json
    def import_csv(self, csv_data):
        data = {"hardware": []}
        read_csv(csv_data=csv_data, class_data=data.get("hardware"), class_obj=Hardware)
        self.import_data(data)

    def import_json(self, json_data):
        data = read_json(json_data)
        self.device_datamodel.import_data(data=data.get("device"))
        self.import_data(data=data.get("hardware"))

    @staticmethod
    def get_all():
        q = Hardware.get_all()
        return q

    # @staticmethod
    # def get_mac_addresses(hardware_id):
    #     q = MacAddressModel.get_by_hardware(hardware_id)
    #     return q

    # @staticmethod
    # def get_nodes(hardware_id):
    #     q = NodeModel.get_by_hardware(hw_id=hardware_id)
    #     return q
    @staticmethod
    def get_by_template(template_id: int):
        q = Hardware.get_by_template(template_id=template_id)
        return q

    @staticmethod
    def get_by_device(device_id: int):
        q = Hardware.get_by_device(device_id=device_id)
        return q

    @staticmethod
    def like_by_serial(serial_number):
        q = Hardware.like_by_serial(serial_number)
        return q

    def purge_data(self, item: Hardware):
        pass
        # try:
        #     nodes = self.get_nodes(item.id)
        #     if nodes:
        #         raise Exception(
        #             f"There are nodes still associate with this hardware.  Please remove the association before deleting."
        #         )
        #     # mac_list = self.get_mac_addresses(item.id)
        #     # if mac_list:
        #     #     self.mac_datamodel.delete_all(mac_list)
        # except Exception as error:
        #     flash(str(error), "error")
        #     abort(404)

    def validate(self, item):
        log = {"hardware": []}
        if len(Hardware.like_by_serial(item.serial_number, getall=True)) > 1:
            msg = f"Serial number {item.serial_number} is not unique."
            log["hardware"].append(msg)
        if not item.serial_number.isalpha():
            msg = f"Serial number {item.serial_number} is not alphanumeric."
            log["hardware"].append(msg)
        if not item.asset_tag.isalpha():
            msg = f"Asset tag {item.serial_number} is not alphanumeric."
            log["hardware"].append(msg)
        if log["hardware"]:
            return log
        else:
            return None

    def validate_all(self):
        items = Hardware.get_all()
        log = {"hardware": []}
        for item in items:
            if len(Hardware.like_by_serial(item.serial_number, getall=True)) > 1:
                msg = f"Serial number {item.serial_number} is not unique."
                log["hardware"].append(msg)
            if not item.serial_number.isalnum():
                msg = f"Serial number {item.serial_number} is not alphanumeric."
                log["hardware"].append(msg)
            if not item.asset_tag.isalnum():
                msg = f"Asset tag {item.asset_tag} is not alphanumeric."
                log["hardware"].append(msg)
        if log["hardware"]:
            return log
        else:
            return None

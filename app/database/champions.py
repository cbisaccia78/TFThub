from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from app import db
from app.database.origins import Origin
from app.database.classes import Classe
from sqlalchemy_json import MutableJson
import random


class Champion(Model):
    __tablename__ = "champions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    origin = relationship("Origin")
    classe = relationship("Classe")
    cost = Column(Integer)
    abilities = Column(MutableJson)

    def __repr__(self):
        return f"{self.device_name()} - {self.template_name()} - {self.serial_number} - {self.asset_tag}"

    def device_name(self):
        if self.device:
            return self.device.name

    def template_name(self):
        if self.template:
            return self.template.name

    @staticmethod
    def add(
            device_id=None,
            template_id=None,
            serial_number=None,
            asset_tag=None,
            info=None,
    ):
        # add a hardware
        hardware = Hardware(
            device_id=device_id,
            template_id=template_id,
            serial_number=serial_number,
            asset_tag=asset_tag,
            info=info,
        )
        db.session.add(hardware)
        db.session.commit()
        return hardware

    def as_dict(self):
        data = {
            "id": self.id,
            "device_id": self.device_id,
            "device": self.device.name if self.device_id else None,
            "template_id": self.template_id,
            "template": self.template.name if self.template_id else None,
            "serial_number": self.serial_number,
            "asset_tag": self.asset_tag,
            "info": self.info,
        }
        return data

    @staticmethod
    def csv_to_dict(row):
        data = {
            "device": row[0],
            "template": row[1],
            "serial_number": row[2],
            "asset_tag": row[3],
            "info": row[4],
        }
        return data

    @staticmethod
    def from_dict(data):
        new_item = Hardware(
            device_id=data.get("device_id", None),
            template_id=data.get("template_id", None),
            serial_number=data.get("serial_number", "Import Error"),
            asset_tag=data.get("asset_tag", None),
            info=data.get("info", None),
        )
        return new_item

    @staticmethod
    def get_fields():
        fields = [
            "id",
            "device_id",
            "device",
            "template_id",
            "template",
            "serial_number",
            "asset_tag",
            "info",
        ]
        return fields

    @staticmethod
    def get_all():
        hardwares = db.session.query(Hardware).all()
        return hardwares

    @staticmethod
    def get(hardware_id):
        hardware = db.session.query(Hardware).filter_by(id=hardware_id).first()
        return hardware

    @staticmethod
    def get_by_serial(serial_number, get_all=False):
        if get_all:
            return db.session.query(Hardware).filter_by(serial_number=serial_number)
        return db.session.query(Hardware).filter_by(serial_number=serial_number).first()

    # @staticmethod
    # def count_by_devicetype(project_id, device_type):
    #     count = None
    #     valid_device = (
    #         device_type == "router"
    #         or device_type == "firewall"
    #         or device_type == "server"
    #         or device_type == "client"
    #     )
    #     if valid_device:
    #         count = (
    #             db.session.query(Hardware)
    #             .filter(Hardware.project_id == project_id)
    #             .join(Device)
    #             .filter(Device.id == Hardware.device_id)
    #             .filter(Device.category == device_type)
    #             .count()
    #         )
    #     return count

    @staticmethod
    def get_by_device(device_id):
        return (
            db.session.query(Hardware)
                .filter_by(device_id=device_id)
                .order_by(Hardware.serial_number)
                .all()
        )

    @staticmethod
    def get_by_template(template_id):
        return (
            db.session.query(Hardware)
                .filter_by(template_id=template_id)
                .order_by(Hardware.serial_number)
                .all()
        )

    @staticmethod
    def get_random_hardware():
        hardwares = db.session.query(Hardware).all()
        return random.choice(hardwares)

    @staticmethod
    def like_by_serial(serial_number, getall=False):
        if getall:
            q = (
                db.session.query(Hardware)
                    .filter(Hardware.serial_number.like(serial_number))
                    .all()
            )
        else:
            q = (
                db.session.query(Hardware)
                    .filter(Hardware.serial_number.like(serial_number))
                    .first()
            )
        return q

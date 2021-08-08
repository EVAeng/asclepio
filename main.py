import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from db.DBHandler import DBHandler


class Doctor(graphene.ObjectType):
    _id = graphene.ID()
    rate = graphene.Float()
    reviews = graphene.List(graphene.String)
    price = graphene.Float()
    specialties = graphene.List(graphene.String)
    name_prefix = graphene.String()
    credential = graphene.String()
    last_name = graphene.String()
    first_name = graphene.String()
    middle_name = graphene.String()
    gender = graphene.String()
    address_1st_line = graphene.String()
    address_2nd_line = graphene.String()
    address_city = graphene.String()
    address_state = graphene.String()
    address_zip_code = graphene.Int()
    address_phone = graphene.String()
    license_number = graphene.String()
    npi = graphene.Int()

    def resolve_id(self, info):
        return self._id

    def resolve_name(self, info):
        return self.name

    def resolve_rate(self, info):
        return self.rate

    def resolve_reviews(self, info):
        return self.reviews

    def resolve_price(self, info):
        return self.price

    def resolve_specialties(self, info):
        return self.specialties

    def resolve_address_zip_code(self, info):
        try:
            return int(self.address_zip_code)
        except Exception as e:
            return 0


class Query(graphene.ObjectType):
    doctors = graphene.List(Doctor)

    def resolve_doctors(self, info):
        with DBHandler() as db:
            doctors_col = db.get_doctors()
            doctors = [Doctor(_id=doc.get("_id"), rate=doc.get("rate"),
                              reviews=doc.get("reviews"), price=doc.get("price"), specialties=doc.get("specialties"),
                              name_prefix=doc.get("name_prefix"), credential=doc.get("credential"), last_name=doc.get("last_name"),
                              first_name=doc.get("first_name"), middle_name=doc.get("middle_name"), gender=doc.get("gender"),
                              address_1st_line=doc.get("address_1st_line"), address_2nd_line=doc.get("address_2nd_line"), address_city=doc.get("address_city"),
                              address_state=doc.get("address_state"), address_zip_code=doc.get("address_zip_code", 0), address_phone=doc.get("address_phone"),
                              license_number=doc.get("license_number"), npi=doc.get("npi"),) for doc in doctors_col.find({})]
        return doctors


app = FastAPI()

app.add_route(
    "/", GraphQLApp(schema=graphene.Schema(query=Query, auto_camelcase=False)))

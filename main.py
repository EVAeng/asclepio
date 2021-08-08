import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from db.DBHandler import DBHandler


class Doctor(graphene.ObjectType):
    _id = graphene.ID()
    name = graphene.String()
    rate = graphene.Float()
    reviews = graphene.List(graphene.String)
    price = graphene.Float()
    specialties = graphene.List(graphene.String)

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


class Query(graphene.ObjectType):
    doctors = graphene.List(Doctor)

    def resolve_doctors(self, info):
        with DBHandler() as db:
            doctors_col = db.get_doctors()
            doctors = [Doctor(_id=doc.get("_id"), name=doc.get("first_name"), rate=doc.get("rate"),
                              reviews=doc.get("reviews"), price=doc.get("price"), specialties=doc.get("specialties")) for doc in doctors_col.find({})]
        return doctors


app = FastAPI()

app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

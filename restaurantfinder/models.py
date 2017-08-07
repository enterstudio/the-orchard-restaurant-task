from datetime import datetime
import logging

from google.appengine.ext import ndb

log = logging.getLogger(__name__)

CUISINE_FIELD = "CUISINE DESCRIPTION"


class Restaurant(ndb.Model):
    name = ndb.StringProperty(required=True)

    address = ndb.StringProperty()
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()
    building = ndb.StringProperty()
    street = ndb.StringProperty()
    boro = ndb.StringProperty()
    zipcode = ndb.StringProperty()

    phone = ndb.StringProperty()
    cuisine = ndb.StringProperty()
    inspection_date = ndb.DateProperty()
    # action = ndb.StringProperty()
    # violation_code = ndb.StringProperty()
    # violation_description = ndb.StringProperty()
    critical_flag = ndb.BooleanProperty()
    score = ndb.IntegerProperty()
    grade = ndb.StringProperty()
    grade_date = ndb.DateProperty()
    record_date = ndb.DateProperty()

    # inspection_type = ndb.StringProperty()

    def to_dict(self, include=None, exclude=None):
        result = super(Restaurant, self).to_dict(include=include,
                                                 exclude=exclude)
        for d in ['inspection_date', 'grade_date', 'record_date']:
            v = getattr(self, d)
            if v is not None:
                result[d] = v.strftime('%m/%d/%y')
            else:
                result[d] = None

        return result

    @staticmethod
    def is_critical(v):
        if v == "Critical":
            return True
        elif v == "Not Critical":
            return False
        return None

    @staticmethod
    def get_date(v):
        if v == '':
            return None
        try:
            return datetime.strptime(v, '%m/%d/%Y')
        except Exception:
            try:
                return datetime.strptime(v, '%m/%d/%y')
            except Exception:
                return None

    @staticmethod
    def get_int(v):
        try:
            return int(v)
        except Exception:
            return 0

    @classmethod
    def create_from_row(cls, row):
        return cls(
            name=row["DBA"],
            phone=row["PHONE"],
            cuisine=row["CUISINE DESCRIPTION"],
            inspection_date=cls.get_date(row["INSPECTION DATE"]),
            building=row["BUILDING"],
            street=row["STREET"],
            boro=row["BORO"],
            zipcode=row["ZIPCODE"],
            # action=row["ACTION"],
            # violation_code=row["VIOLATION CODE"],
            # violation_description=row["VIOLATION DESCRIPTION"],
            critical_flag=cls.is_critical(row["CRITICAL FLAG"]),
            score=cls.get_int(row["SCORE"]),
            grade=row["GRADE"],
            grade_date=cls.get_date(row["GRADE DATE"]),
            record_date=cls.get_date(row["RECORD DATE"]),
            # inspection_type=row["INSPECTION TYPE"]
        ).put()

    @classmethod
    def get_best_rated(cls):
        return cls.query().fetch()

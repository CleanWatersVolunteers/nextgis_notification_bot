
class new_rec_manager:

    @classmethod
    def init(cls):
        cls.current_record_id = 0
        cls.potential_next_record_id = 0
        with open("storage_record_number_0.dat", "r") as f:
            cls.current_record_id = int(f.read())

    @classmethod
    def get_new_features(cls, features):
        ret = []
        fe = features["features"]
        for f in fe:
            if f["type"] == "Feature" and int(f["id"]) > cls.current_record_id:
                ret.append(f)
                if int(f["id"]) > cls.potential_next_record_id:
                    cls.potential_next_record_id = int(f["id"])
        return ret

    @classmethod
    def update_current_record_id(cls):
        cls.current_record_id = cls.potential_next_record_id
        with open("storage_record_number_0.dat", "w") as f:
            f.write(str(cls.current_record_id))
        with open("storage_record_number_1.dat", "w") as f:
            f.write(str(cls.current_record_id))





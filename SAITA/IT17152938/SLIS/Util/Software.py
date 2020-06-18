from Util.DBConnection import DBConnection


class Software:
    db = None

    @classmethod
    def __init__(self):
        self.db = DBConnection()

# get all software list from db
    @classmethod
    def get_all_software(cls):
        return cls.db.execute_query('Select * from Software where del=%s', ('0',))

# get search software list from db
    @classmethod
    def get_search_software(cls, soft):
        soft_ser='%'+soft+'%'
        return cls.db.execute_query('Select * from Software where LOWER(`name`) LIKE %s and del=%s', (soft_ser, '0'))

# get all software version list from db
    @classmethod
    def get_all_version(cls, soft_id):
        return cls.db.execute_query('Select * from Version where del=%s and soft_id=%s order by id desc', ('0', str(soft_id)))

# get all dependency list for version from db
    @classmethod
    def get_dependency(cls, ver_id):
        return cls.db.execute_query('Select * from dependency where del=%s and verId=%s', ('0', ver_id))

# get all path list for version from db
    @classmethod
    def get_path(cls, ver_id):
        return cls.db.execute_query('Select * from path where del=%s and verId=%s', ('0', ver_id))

# get all path list for version from db
    @classmethod
    def get_install_step(cls, ver_id):
        return cls.db.execute_query('Select * from path where del=%s and verId=%s', ('0', ver_id))

# get software name using software id
    @classmethod
    def get_soft_name_by_id(cls, soft_id):
        return cls.db.execute_query('Select `name` from Software where del=%s and id=%s', ('0', str(soft_id)))

# get software version number using version id
    @classmethod
    def get_soft_ver_by_id(cls, ver_id):
        return cls.db.execute_query('Select v_no from Version where del=%s and id=%s', ('0', str(ver_id)))

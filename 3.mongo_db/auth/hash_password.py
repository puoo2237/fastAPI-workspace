import bcrypt

class HashPwd:
    def create_hash(self, pwd:str)->str:
        hash_pwd = bcrypt.hashpw(
            pwd.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hash_pwd.decode("utf-8")
    
    def verity_hash(self, in_pwd:str, db_pwd:str)->str:
        return bcrypt.checkpw(in_pwd.encode("utf-8"), db_pwd.encode("utf-8"))
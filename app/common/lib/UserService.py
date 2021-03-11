import random, string, hashlib, base64


class UserService(object):

    @staticmethod
    def gene_auth_code(user_info=None):
        m = hashlib.md5()
        auth_str = "%s-%s-%s" % (
            user_info.id, user_info.name, user_info.password)
        m.update(auth_str.encode("utf-8"))

        return m.hexdigest()

    @staticmethod
    def gene_pwd(pwd):
        # 先进行密码的 Base64 编码，与salt拼接后进行哈希运算得到最终密码
        m = hashlib.md5()
        pwd_str = "%s" % (base64.encodebytes(pwd.encode("utf-8")))
        m.update(pwd_str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def gene_salt(length=16):
        key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(key_list)

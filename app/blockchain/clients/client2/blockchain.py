import hashlib
import json
from typing import Dict, Any


class BlockChain:
    def __init__(self):
        self.chain = []
        print("正在从文件中加载区块链信息...")
        chain_json = self.load_file()
        if chain_json["length"] == 0 or self.valid_chain(chain_json["chain"]) is False:
            # 创建创世块
            print("文件验证失败，即将生成新的区块链")
            self.new_block({}, proof=100)
        else:
            print("文件验证成功")
            self.chain = chain_json["chain"]

    def load_file(self):
        try:
            with open("blockchain.json", "r", encoding="utf-8") as fr:
                data = json.load(fr)
                return data
        except FileNotFoundError as e:
            self.update_file()
            with open("blockchain.json", "r", encoding="utf-8") as fr:
                data = json.load(fr)
                return data

    def update_file(self):
        with open("blockchain.json", "w", encoding="utf-8") as fw:
            json.dump(self.full_chain(), fw, indent=4)
            print("保存成功")

    def valid_chain(self, chain) -> bool:
        """
        验证区块链的信息是否正确

        :param chain: 一个区块链
        :return: 正确返回True，否则返回False
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                print("前置哈希验证失败")
                return False
            # Check that the hash of Work is correct
            if not self.valid_proof(current_index + 1, block["content"], block["proof"], block["previous_hash"]):
                print("工作量证明验证失败")
                return False

            last_block = block
            current_index += 1
        print("区块链校验通过")
        return True

    def new_block(self, data, proof, index=None) -> Dict[str, Any]:

        """
        生成新块

        :param data: 区块中保存的数据
        :param proof: 计算得到的工作量证明
        :param index: 新区块的索引
        :return: 新的区块
        """
        if index is None:
            index = len(self.chain) + 1
        previous_hash = "0000xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        if self.last_block:
            previous_hash = self.hash(self.last_block)

        block = {
            "index": index,
            "content": data,
            "proof": proof,
            "previous_hash": previous_hash
        }
        temp_chain = list(self.chain[0:index])
        temp_chain.append(block)
        if self.valid_chain(temp_chain):
            self.chain = list(temp_chain)
            print("新区块创建并验证成功，正在保存")
            self.update_file()

        return block

    @staticmethod
    def new_data(op_id, operator, option, commodity, time):
        """
        生成新操作信息，信息将加入到下一个待挖的区块中

        :param time: 操作时间
        :param op_id: 操作id
        :param operator: 商品的操作者
        :param option: 操作类型
        :param commodity: 被操作的商品
        :return: 创建好的操作信息
        """

        data = (
            {
                "id": op_id,
                "operator": operator,
                "option": option,
                "commodity": commodity,
                "time": time
            }
        )
        return data

    @staticmethod
    def hash(block) -> str:
        """
        生成块的 SHA-256 hash值

        :param block: Block
        :return: 哈希值
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        if len(self.chain) >= 1:
            return self.chain[-1]
        else:
            return None

    def proof_of_work(self, block_data) -> int:
        """
        简单的工作量证明：
        - 查找一个 p' 使得 hash(pp') 以4个0开头
        - p 是上一个块的证明，p' 是当前的证明
        :param block_data: 上一个证明
        :return: 查找到的证明
        """
        guss_proof = 0
        while self.valid_proof(len(self.chain) + 1, block_data, guss_proof) is False:
            guss_proof += 1
            if guss_proof % 1000 == 0:
                print(guss_proof, end=",")
            if guss_proof % 10000 == 0:
                print("\n")

        return guss_proof

    def valid_proof(self, index, data, proof: int, previous_hash=None) -> bool:
        """
        验证证明: 是否hash(last_proof, proof)以4个0开头
        :param previous_hash:
        :param index:
        :param data: 前一个区块的哈希值
        :param proof: Current Proof
        :return: True if correct, False if not.
        """
        if previous_hash is None:
            previous_hash = self.hash(self.last_block)
        block = {
            "index": index,
            "content": data,
            "proof": proof,
            "previous_hash": previous_hash
        }
        guess_hash = self.hash(block)
        # print(guess_hash)
        if guess_hash.startswith("0000"):
            return True
        else:
            return False

    def full_chain(self):
        data = {
            'chain': self.chain,
            'length': len(self.chain)
        }
        return data


def create_chain():
    op_data = chain.new_data(2, "操作者", "操作类型", "商品", "time")
    op_data = [chain.new_data(2, "操作者", "操作类型", "商品", "time"), chain.new_data(2, "操作者", "操作类型", "商品", "time"),
               chain.new_data(2, "操作者", "操作类型", "商品", "time")]
    new_proof = chain.proof_of_work(op_data)
    chain.new_block(data=op_data, proof=2321084, index=4)


if __name__ == '__main__':
    chain = BlockChain()

    create_chain()
    temp = json.dumps(chain.full_chain())
    print(temp)

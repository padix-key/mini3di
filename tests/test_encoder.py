import unittest

import Bio.PDB
from mini3di import Encoder, PartnerIndexEncoder

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


class TestPartnerIndexEncoder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.encoder = PartnerIndexEncoder()
        cls.parser = Bio.PDB.PDBParser(QUIET=True)

    @classmethod
    def get_structure(cls, name):
        path = resource_files(__package__).joinpath("data", f"{name}.pdb")
        return cls.parser.get_structure(name, path)

    def test_encode_1xso_chainA(self):
        structure = self.get_structure("1xso")
        partners = self.encoder.encode_chain(structure[0]["A"])
        self.assertListEqual(
            list(partners[1:-1]),
            # fmt: off
            [
                17, 145, 15, 143, 13, 141, 6, 53, 8, 11, 12, 32, 5, 30, 3, 28, 
                1, 26, 20, 19, 20, 21, 98, 98, 96, 18, 94, 16, 92, 14, 90, 12, 
                89, 89, 117, 35, 85, 37, 83, 115, 80, 113, 79, 111, 57, 57, 
                110, 143, 50, 53, 50, 50, 50, 55, 56, 55, 45, 45, 132, 43, 77, 
                77, 62, 62, 66, 75, 131, 76, 122, 80, 97, 73, 74, 73, 66, 68, 
                62, 99, 43, 41, 70, 119, 39, 91, 37, 87, 86, 87, 33, 31, 84, 
                29, 94, 27, 94, 25, 71, 23, 78, 106, 23, 107, 104, 103, 104, 
                100, 102, 144, 144, 47, 44, 142, 42, 139, 40, 136, 35, 136, 82, 
                134, 134, 69, 130, 125, 124, 127, 128, 127, 132, 120, 67, 59, 
                120, 120, 136, 116, 138, 137, 114, 7, 6, 112, 4, 109, 2, 109, 
                148, 147
            ]
            # fmt: on
        )


class TestEncoder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.encoder = Encoder()
        cls.parser = Bio.PDB.PDBParser(QUIET=True)

    @classmethod
    def get_structure(cls, name):
        path = resource_files(__package__).joinpath("data", f"{name}.pdb")
        return cls.parser.get_structure(name, path)

    def test_encode_3bww(self):
        structure = self.get_structure("3bww")
        states = self.encoder.encode_chain(structure[0]["A"])
        sequence = self.encoder.build_sequence(states)
        self.assertEqual(
            sequence,
            "DKDFFEAAEDDLVCLVVLLPPPACPQRQAYEDALVVQVPDDPVSVVSVVNSLVHHAYAYEYEAQQL"
            "LDDPQGDVVSLVSVLVCCVVSVPQEYEYENDPPDADALDVVSLVSSLVSQLVSCVSSVGAYAYEDA"
            "ADQDHDPRHPDDVLVSRQSNCVSNVHAHAYELVRLVRCCVRPVPDDSLVSLVRHPLQRHQHYEYQV"
            "VSVVSVLVNLVDHQAHHYYYHDYPDDVVVNSVVRVVSRVSNVVSCVVVVHYIDMD",
        )

    def test_encode_3bww_masked(self):
        structure = self.get_structure("3bww.masked")
        states = self.encoder.encode_chain(structure[0]["A"])
        sequence = self.encoder.build_sequence(states)
        self.assertEqual(
            sequence,
            "DKDFFEAAEDDLVCLVVLLPPPACPQRQAYEDALVVQVPDDPVSVVSVVNSLVHHAYAYEYEAQQL"
            "DDDPQGDVVSLVSVLVCCVVSVPQEYEYENDPPDADALDPVDDDSSLVSQLVSCVSSVGAYAYEDA"
            "ADQDHDPRHPDDVLVSRQVSCVSNVHAHAYELVRLVRCCVRPVPDDSLVSLVRHPLQRHQHYEYQV"
            "VSVVSVLVNLVDHQAHHYYYHDYPDDVVVNSVVRVVSRVSNVVSCVVVVHYIDMD",
        )

    def test_encode_8crb(self):
        structure = self.get_structure("8crb")

        states = self.encoder.encode_chain(structure[0]["A"])
        sequence = self.encoder.build_sequence(states)
        self.assertEqual(
            sequence,
            "DWAKDKDWADEDAAQAKTKIKMATPPDLLQDFFKFKWFDAPPDDIDGQAPGACPSPPLADDVHHHH"
            "GKGWHDDSVRRMIMIMGGNDDQVVFGKMKMFTADDADPQVVVPDGDDTDDMHDIDTYGHPPDDFFA"
            "WDKDKDQDDPVPCPVQKPKIKMKTDDGDDDDKDKAWLVNPGDPQKDDFDWDADPVRGIIDMIIGMD"
            "GNVCFQVGFTKIWMAGVVVRDIDIDGGHD",
        )

        states = self.encoder.encode_chain(structure[0]["B"])
        sequence = self.encoder.build_sequence(states)
        self.assertEqual(
            sequence,
            "DAAKDFDQQEEEAAQAKDKGWIFAADVPPVPDAFWKWWDAPPDDIDTAADPNQAGDPVDHSQKGWD"
            "ADHGITIIMGGRDDNSRQGFIWRAQPDDPDHNGHTDDTHGYYHCPDDQDDKDKDWDDAAVVVLVVL"
            "FGKTKIKIDDGDDPPKDKFKDLQNHTDDAQWDWDDWDLDPVRTIMTMIIRRDGVVSCVVSQKMKMW"
            "IDDDVHTDIDMDGNVVHD",
        )

        states = self.encoder.encode_chain(structure[0]["C"])
        sequence = self.encoder.build_sequence(states)
        self.assertEqual(
            sequence,
            "DPCVLVVLVLQLVLVVLLLVVVVVVLVVCVVVLFKDWQDPVHDWQLACVSPDHDCPDCCSVPGSNN"
            "VQQCPKPLDDVTATNQSVQQIDDGDLDHDDDDDTIQGCPPPVRCSVVVVVVSVVSVVVSVVSCVVS"
            "VVVVVVD",
        )

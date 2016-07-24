import requests
from bs4 import BeautifulSoup


class FreeMTI():
    def __init__(self):
        pass

    def query(self, text):
        response = requests.post("https://ii.nlm.nih.gov/cgi-bin/II/Interactive/interactiveMTI.pl", files={
            "InputText": (None, text),
            "Filtering": (None, "opt1_DCMS"),
            "showDUIs": (None, "showDUIs"),
            "Output": (None, "Detail"),
            "Advanced": (None, "0"),
            "topn": (None, "25"),
            "mm1": (None, "7"),
            "pub": (None, "2"),
            "trg": (None, "0"),
            "cit": (None, "10"),
            "IM": (None, "1.00"),
            "NIM": (None, "0.80"),
            "dir": (None, "1.00"),
            "atx": (None, "1.00"),
            "par": (None, "0.90"),
            "chd": (None, "0.75"),
            "sib": (None, "0.70"),
            "oth": (None, "0.50"),
            "cot": (None, "10000"),
            "ti": (None, "20"),
            "rel": (None, "100"),
            "emp_hstar": (None, "0.00"),
        }, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        })

        if response.status_code == 200:
            return self.parse_response(response.text)
        raise ConnectionError("Problem with response from MTI")

    def parse_response(self, text):
        content = BeautifulSoup(text, "html.parser")
        pre = content.find_all("pre")[-1]
        for tag in pre.find_all("b"):
            tag.clear()

        return  pre.get_text().strip().split("\n")


if __name__ == "__main__":
    fm = FreeMTI()
    print(fm.query(
        "A 94 year old female with hx recent PE/DVT, atrial fibrillation, CAD presents with fever and abdominal pain. "
        "An abdominal CT demonstrates a distended gallbladder with gallstones and biliary obstruction with several "
        "CBD stones.")
    )

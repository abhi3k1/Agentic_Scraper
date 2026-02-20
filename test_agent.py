import sys
import pathlib
import json

# make src importable
sys.path.append(str(pathlib.Path(__file__).resolve().parent / "src"))

from agent.tools.extractor import extract_data
from agent.storage.database import init_db, save_extraction

html = "<html><body><h1>Test Title</h1><div class='price'>$9.99</div></body></html>"
selectors = {"title": "h1", "price": ".price"}

init_db()
extracted = extract_data(html, selectors)
id_ = save_extraction("test://local", extracted)
print(json.dumps({"id": id_, "data": extracted}))

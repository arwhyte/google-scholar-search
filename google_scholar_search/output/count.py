import umpyutl as umpy

filepath = "./nyt-articles-star_wars-20230406T0932.json"
data = umpy.read.from_json(filepath)
print(f"Length = {len(data)}")
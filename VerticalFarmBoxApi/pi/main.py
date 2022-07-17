from greenhouse_box import GreenhouseBox

box = GreenhouseBox("U38.1", "38.01", "Box1")

box.find_backend()
if box.register_to_backend():
    box.run()



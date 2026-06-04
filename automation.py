# sub-classes of automation:
# browser automation
# documentation automation
#


class Automation:
    def __init__(self):
        self.name = ""
        self.is_running = False

    def start(self):
        self.is_running = True
        self.run()

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")

    def stop(self):
        self.is_running = False

    def status(self) -> dict:
        return {"name": self.name, "is_running": self.is_running}

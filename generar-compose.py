import yaml
import argparse


class Server(yaml.YAMLObject):
    yaml_tag = "!Server"

    def __init__(self):
        self.container_name = "server"
        self.image = "server:latest"
        self.entrypoint = "python3 /main.py"
        self.environment = ["PYTHONUNBUFFERED=1", "LOGGING_LEVEL=DEBUG"]
        self.networks = ["testing_net"]
        self.volumes = ["./server/config.ini"]

    def __repr__(self):
        return (
            "%s(container_name=%r, image=%r, entrypoint=%r, environment=%r, networks=%r, volumes=%r)"
            % (
                self.__class__.__name__,
                self.container_name,
                self.image,
                self.entrypoint,
                self.environment,
                self.networks,
                self.volumes,
            )
        )


class Client(yaml.YAMLObject):
    yaml_tag = "!Client"

    def __init__(self, number):
        self.container_name = f"client{number}"
        self.image = "client:latest"
        self.entrypoint = "/client"
        self.environment = [f"CLI_ID={number}", "CLI_LOG_LEVEL=DEBUG"]
        self.networks = ["testing_net"]
        self.depends_on = ["server"]
        self.volumes = ["./client/config.yaml"]

    def __repr__(self):
        return (
            "%s(container_name=%r, image=%r, entrypoint=%r, environment=%r, networks=%r, depends_on=%r, volumes=%r)"
            % (
                self.__class__.__name__,
                self.container_name,
                self.image,
                self.entrypoint,
                self.environment,
                self.networks,
                self.depends_on,
                self.volumes,
            )
        )


class TestingNet(yaml.YAMLObject):
    yaml_tag = "!TestingNet"

    def __init__(self):
        self.ipam = {"driver": "default", "config": [{"subnet": "172.25.125.0/24"}]}

    def __repr__(self):
        return "%s(ipam=%r)" % (
            self.__class__.__name__,
            self.ipam,
        )


def generar_data(n_clientes):
    data = {
        "name": "tp0",
        "services": {},
        "networks": {},
    }

    data["services"]["server"] = Server()

    for n in range(1, n_clientes + 1):
        data["services"][f"client{n}"] = Client(number=n)

    data["networks"]["testing_net"] = TestingNet()

    return data


def main():
    argumentos = parsear_argumentos()

    data = generar_data(argumentos.cantidad_de_clientes)

    with open(argumentos.archivo_de_salida, "w+") as stream:
        yaml.dump(data, stream)


def parsear_argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("archivo_de_salida")
    parser.add_argument("cantidad_de_clientes", type=int)

    return parser.parse_args()


main()

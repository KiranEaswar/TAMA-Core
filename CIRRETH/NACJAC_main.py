from NACJAC_configurator import NACJAC_Config
from NACJAC_netrun import NACJAC_Generator

if __name__ == "__main__":
    config = NACJAC_Config()
    generator = NACJAC_Generator(config)

    print("\n=== NACJAC OUTPUT ===")
    output = generator.generate_text("Doesn't Hemantha suck? ")
    print(output)

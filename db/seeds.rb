# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

#
# Categories
#

Category.create(name: "Boards / Controllers / PLC's")
Category.create(name: "Relays")
Category.create(name: "Springs")
Category.create(name: "Solenoids")
Category.create(name: "Shock Absorbers")
Category.create(name: "Turnstile Maintenance Tools")
Category.create(name: "The Parts Bin")
Category.create(name: "Microswitches & Sensors")
Category.create(name: "Lamps / Switches & Enclosures")
Category.create(name: "Power Supply Parts")
Category.create(name: "Sliding Gate Parts")
Category.create(name: "Used Turnstiles")
Category.create(name: "Bearings, Rollers & Cams")
Category.create(name: "Pawls, Linkages, Studs & Hardware")
Category.create(name: "Mechanical Assemblies")
Category.create(name: "Serial Port Interface")
Category.create(name: "New Turnstiles")
Category.create(name: "Upgrade Kits")

#
# Manufacturers
#

Manufacturer.create(name: "Robot")
Manufacturer.create(name: "Burle")
Manufacturer.create(name: "Philips")
Manufacturer.create(name: "Tomsed")
Manufacturer.create(name: "Boon Edam")
Manufacturer.create(name: "Alvarado")
Manufacturer.create(name: "Controlled Access")
Manufacturer.create(name: "Ingress Controls")
Manufacturer.create(name: "Perey")
Manufacturer.create(name: "Automatic Systems")

#
# Styles
#

Style.create(name: "Full Height")
Style.create(name: "Gate")
Style.create(name: "Optical")

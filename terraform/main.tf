provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "Alien"
  location = "Australia Central"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

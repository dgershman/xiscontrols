class Api::ManufacturersController < ApplicationController

  def index
    @manufacturers = Manufacturer.all
  end
  
end
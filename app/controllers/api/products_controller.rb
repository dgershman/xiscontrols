class Api::ProductsController < ApplicationController

  def index
    @products = Product.all.includes(:categories, :styles, :manufacturers, :variants)
  end
  
end
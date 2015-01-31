class Product < ActiveRecord::Base
  belongs_to :category  
  belongs_to :manufacturer
  has_and_belongs_to_many :styles

  has_many :product_variants
  has_many :product_images
  has_many :product_documents  
end

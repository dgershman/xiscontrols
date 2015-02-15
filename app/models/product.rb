class Product < ActiveRecord::Base
  has_and_belongs_to_many :categories
  has_and_belongs_to_many :manufacturers
  has_and_belongs_to_many :styles

  has_many :variants, dependent: :delete_all
  has_many :images
  has_many :documents

  accepts_nested_attributes_for :categories
  accepts_nested_attributes_for :manufacturers
  accepts_nested_attributes_for :styles
  accepts_nested_attributes_for :variants
end

class CompanyLocation < ActiveRecord::Base
  belongs_to :company
  has_many :contacts
end

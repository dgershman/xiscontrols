ActiveAdmin.register Product do  

  # See permitted parameters documentation:
  # https://github.com/activeadmin/activeadmin/blob/master/docs/2-resource-customization.md#setting-up-strong-parameters
  #
  permit_params :description, category_ids: [], manufacturer_ids: [], style_ids: [], 
    variants_attributes: [:id, :product_id, :sku, :description, :price, :_destroy]
  #
  # or
  #
  # permit_params do
  #   permitted = [:permitted, :attributes]
  #   permitted << :other if resource.something?
  #   permitted
  # end

  show do
    attributes_table do
      row :name
      row :description      
    end
    panel 'Categories' do
      product.categories.each do |category|
        status_tag category.name, :ok        
      end
    end
    panel 'Manufacturers' do
      product.manufacturers.each do |manufacturer|
        status_tag manufacturer.name, :ok
      end
    end
    panel 'Styles' do
      product.styles.each do |style|
        status_tag style.name, :ok
      end
    end
    panel 'Variants' do
      table_for product.variants do
        column :sku
        column :description        
        column :price
        column :weight
      end    
    end    
  end

  # t.string :sku, null: false, unique: true
  # t.string :description
  # t.decimal :price, precision: 8, scale: 2, default: 0.0, null: false

  form do |f|
    f.semantic_errors    
    f.inputs do
      f.input :name
      f.input :description
      f.input :categories, as: :check_boxes, collection: Category.all.order(:name)
      f.input :manufacturers, as: :check_boxes, collection: Manufacturer.all.order(:name)
      f.input :styles, as: :check_boxes, collection: Style.all.order(:name)      
    end
    f.inputs do
      f.has_many :variants, heading: 'Variants', allow_destroy: true, new_record: true do |v|        
        v.input :sku, as: :string
        v.input :description, as: :text        
        v.input :price, as: :number
        v.input :weight, as: :number
      end
    end
    f.actions
  end

end

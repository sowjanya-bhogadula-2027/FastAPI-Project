import React from 'react';
import './TaglineSection.css';

const TaglineSection = () => {
  return (
    <div className="tagline-card">
      <div className="tagline-content">
        <h3>Product Management Inventory</h3>
        <li style={{textAlign: "left"}}>Add new products to the inventory system.</li>
        <li style={{textAlign: "left"}}>Update existing products in the system.</li>
        <li style={{textAlign: "left"}}>Delete products from the inventory system.</li>
        
      </div>
    </div>
  );
};

export default TaglineSection;

-- MariaDB Database Schema for ebay_inventory
-- This file defines the tables used to track eBay listings, inventory, sales, bids, shipping, and feedback.

CREATE DATABASE IF NOT EXISTS ebay_inventory;
USE ebay_inventory;

-- 1. Track physical inventory and scheduled listing details
CREATE TABLE IF NOT EXISTS inventory_items (
    sku VARCHAR(50) NOT NULL,
    title VARCHAR(80) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT UNSIGNED DEFAULT 1,
    weight_lbs DECIMAL(5, 2) DEFAULT NULL,
    carrier VARCHAR(50) DEFAULT NULL,
    shipping_service VARCHAR(100) DEFAULT NULL,
    scheduled_at DATETIME DEFAULT NULL,        -- Planned date/time to list on eBay
    ebay_listing_id VARCHAR(50) DEFAULT NULL,  -- Populated after publishing to eBay
    status VARCHAR(20) DEFAULT 'draft',        -- draft, scheduled, active, sold, ended
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (sku)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Store local/remote image paths or URLs associated with inventory items
CREATE TABLE IF NOT EXISTS item_pictures (
    id INT AUTO_INCREMENT NOT NULL,
    sku VARCHAR(50) NOT NULL,
    picture_url VARCHAR(2048) NOT NULL,        -- Local path or eBay Picture Services (EPS) URL
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_pictures_sku FOREIGN KEY (sku) 
        REFERENCES inventory_items (sku) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Track eBay orders, buyer details, shipment tracking, and feedback status
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) NOT NULL,             -- eBay-provided Order ID
    sku VARCHAR(50) NOT NULL,
    buyer_username VARCHAR(100) DEFAULT NULL,
    sale_price DECIMAL(10, 2) NOT NULL,
    shipping_cost DECIMAL(10, 2) DEFAULT 0.00,
    carrier VARCHAR(50) DEFAULT NULL,
    tracking_number VARCHAR(100) DEFAULT NULL,
    shipping_status VARCHAR(30) DEFAULT 'pending', -- pending, shipped, delivered, cancelled
    feedback_left BOOLEAN DEFAULT FALSE,
    feedback_received BOOLEAN DEFAULT FALSE,
    sold_at DATETIME NOT NULL,                 -- Date/time order was completed on eBay
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_sku FOREIGN KEY (sku) 
        REFERENCES inventory_items (sku) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Track live bids for auction style listings
CREATE TABLE IF NOT EXISTS auction_bids (
    bid_id VARCHAR(50) NOT NULL,                -- eBay bid ID or transaction identifier
    ebay_listing_id VARCHAR(50) NOT NULL,      -- Target listing
    bidder_username VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    bid_time DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bid_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

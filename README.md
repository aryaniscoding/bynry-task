# Inventory Management System - Bynry Case Study

**Author:** Aryan Sahu  
**Role:** Backend Engineering Intern Candidate  
**Date:** 06/01/2026

## Overview
This is my submission for the Bynry backend internship task. I solved all three parts: debugging the broken code, designing the database, and building the low stock API.

---

## Part 1: Code Review & Debugging

**The Issues:**
The original code for creating products was kinda messy. It didn't check for errors, it was saving data in two steps (which is risky if the database crashes in between), and it linked products to only one warehouse, which is wrong because products can be everywhere.

**My Fixes:**
I rewrote the code to make it safer:
1.  **All or Nothing:** I made it save everything in one go (Atomic Transaction) so we don't get bad data.
2.  **Checking Inputs:** Added checks so users can't send negative prices or missing names.
3.  **Correct Logic:** I removed `warehouse_id` from the Product table so a product can exist in many warehouses.
4.  **Math Fix:** Used `Decimal` instead of float because computer math is bad with money.
5.  **Handling Errors:** Added a try/except block to catch duplicate SKUs.

---

## Part 2: Database Design

**My Design:**
I made a simple SQL schema to handle everything properly.

**Main Tables:**
*   `products`: Just the item details like name and SKU.
*   `warehouses`: Where the stuff is kept.
*   `inventory`: This links Products to Warehouses and counts the stock.
*   `inventory_log`: Keeps a history of every change so we know where stock went.
*   `suppliers`: Who provides the products.

**Assumptions:**
*   I assumed SKUs are unique for everyone in the app.
*   Prices are the same everywhere.
*   Suppliers can sell to anyone.

---

## Part 3: Low Stock Alerts API

**The Goal:**
Make an API `GET /api/companies/{id}/alerts/low-stock` to show items that are running out.

**How I did it:**
I didn't use complex sub-queries because they are hard to read. Instead, I did it in steps:
1.  First, get all the inventory for the company.
2.  Then loop through it in Python to apply the rules.
    *   **Thresholds:** If item is expensive (>1000), warn at 5 units. If cheap, warn at 20.
    *   **Dead Stock:** If nobody bought it in 30 days, I just ignore it so we don't spam the user.
3.  Finally, I calculate `days_until_stockout` using the recent sales average.

**Edge Cases:**
*   Handled division by zero (if sales are 0).
*   Handled missing suppliers (if a product has no supplier yet).
*   Ignored dead stock that isn't selling.

---

**Contact:**  
Aryan Sahu  
aryansahu2705@gmail.com  
PICT EnTC (Third Year)

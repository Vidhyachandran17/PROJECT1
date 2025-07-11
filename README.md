# PhonePe Pulse - Data

The Indian digital payments story has truly captured the world’s imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-art payments infrastructure built as Public Goods championed by the central bank and the government. PhonePe started in 2016 and has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for definitive data sources on digital payments in India without much success. As a way of giving back to the data and developer community, we decided to open the anonymised aggregate data sets that demystify the what, why and how of digital payments in India. Licensed under the [CDLA-Permissive-2.0 open data license](https://github.com/PhonePe/pulse/blob/master/LICENSE), the PhonePe Pulse Dataset API is a first of its kind open data initiative in the payments space.

## Announcements

:star2: Data for Q3 (_July, August, September_) and Q4 (_October, November, December_) of 2024 has been added and is available for consumption.

## Table of Contents

- [PhonePe Pulse - Data](#phonepe-pulse---data)
  - [Announcements](#announcements)
  - [Table of Contents](#table-of-contents)
  - [Goal](#goal)
  - [Guide](#guide)
  - [Documentation](#documentation)
    - [Folder Structure](#folder-structure)
    - [JSON Structure / Syntax](#json-structure--syntax)
      - [Aggregated](#1-aggregated)
      - [Map](#2-map)
      - [Top](#3-top)
  - [FAQs](#faqs)
  - [LICENSE](#license)

## Goal

Our goal is to share this data with everyone (license below), so that you can build your own understanding, insights and visualization on how digital payments have evolved over the years in India.

## Guide

This [data](https://github.com/PhonePe/pulse/tree/master/data) has been structured to provide details of the following three sections with data cuts on **Transactions**, **Users** and **Insurance** of PhonePe Pulse - Explore tab:

1. **Aggregated** - Aggregated values of various payment categories as shown under *Categories* section.
2. **Map** - Total values at the State and District levels.
3. **Top** - Totals of top States / Districts / Pin Codes.

All the data provided in these folders is in JSON format. For more details on the structure/syntax, refer to the [JSON Structure / Syntax](#json-structure--syntax) section.

## Documentation

### Folder Structure

Visit the [data](https://github.com/PhonePe/pulse/tree/master/data) folder for the below structure. Each top-level folder (`aggregated`, `map`, and `top`) contains subfolders for **transactions**, **users**, and **insurance**.

Data is grouped by:

- **Country** → India
- **Year** (within India folder)
- **State** (optional) → which also contains year-wise folders

Each year folder contains four `.json` files named `1.json`, `2.json`, `3.json`, and `4.json` for each quarter respectively.

**Example**: `data/aggregated/transaction/country/india/2018/1.json` → Data for Jan–Mar 2018

### JSON Structure / Syntax

#### 1. Aggregated

- **Transactions**: Total count and value per payment category
- **Users**: Registered users and app opens, categorized by device
- **Insurance**: Total count and value of insurance transactions

#### 2. Map

- **Transaction Hover Data**: Total transaction count and value per state/district
- **User Hover Data**: Registered users and app opens per state/district
- **Insurance Hover Data**: Insurance count and value per state/district

#### 3. Top

- Top **states**, **districts**, and **pin codes** by:
  - Transaction count and value
  - Registered users and app opens
  - Insurance count and value

## FAQs

Check out the [GitHub Issues](https://github.com/PhonePe/pulse/issues) or reach out via discussions if you have queries about using the data.

## LICENSE

Licensed under the [CDLA-Permissive-2.0](https://github.com/PhonePe/pulse/blob/master/LICENSE) open data license.

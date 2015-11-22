---
layout: post
title:  "Dump MySQL Functions and Stored Procedures"
date:   2014-03-15 11:43:54
categories: MySQL
---

A plain mysqldump command without any options would just dump your tables and the data but not your functions and stored procedures.

If you want functions or procedures to be dumped along with your data,

`mysqldump <mysqldump options> --routines dump.sql`

If you want to dump only your functions and procedures –

`mysqldump --routines --no-create-db --no-create-info --no-data --skip-opt database > dump_without_data.sql`

Importing the dump into another mysql

`mysql <  dump_without_data.sql`

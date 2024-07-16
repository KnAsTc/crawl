#title dict

'''
露天 SELL
0 - X

1 - TIME format YYYY/MM/DD

2 - Proudct Name

3 - per Product price

4 - Number of Products

5 - SUM of price

6 - Seller

7 - X

8 - status

9 - X
'''
dict_ru_sell={
"t1":"日期",
"t2":"物品名稱",
"t3":"單一價錢",
"t4":"數量",
"t5":"總價",
"t6":"賣家帳號",
"t8":"狀態"
}
for i in range(8):
    print(f"t{i}")
    print(dict_ru_sell.get(f"t{i}"))


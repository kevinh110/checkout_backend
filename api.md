# Expected Functionality

## Get all items

[GET] /api/items/

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "knife",
      "stock": 1,
      "price": 5
    },
    {
      "id": 2,
      "name": "milk",
      "stock": 1,
      "price": 5
    }
    ...
  ]
}
```


## Create an item

[POST] /api/items/

Request:

```json
{
  "name": <USER INPUT>,
  "price": <USER INPUT>,
  "stock": <USER INPUT>
}
```


Response:

```json
{
  "success": true,
  "data": {
    "id": <ID>,
    "name": <USER INPUT FOR NAME>,
    "stock": <USER INPUT FOR STOCK>,
    "price": <USER INPUT FOR PRICE>
  }
}
```

## Change item Price

[POST] /api/items/<int:item_id>/

Request:
```json
{
  "price": <USER INPUT>,
}
```


Response:
```json
{
    "success": true,
    "data": {
        "id": <ITEM_ID>,
        "name": <NAME>,
        "stock": <STOCK>,
        "price": <USER INPUT FOR PRICE>
    }
}
```

## Create Buyer

[POST] /api/buyers/

Request:

```json
{
	"username": <USER INPUT>,
	"balance": <USER INPUT>
}
```

Response:

```json
{
    "success": true,
    "data": {
        "id": <ID>,
        "username": <USER INPUT FOR USERNAME>,
        "balance": <USER INPUT FOR BALANCE>,
        "cart": [
            {
                "total": 0,
                "items": []
            }
        ],
        "orders": []
    }
}
```

## Get All Buyers

[GET] /api/buyers/

Response:

```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "username": "susan",
            "balance": 5,
            "cart": [<SERIALIZED CART>],
            "orders": [<SERIALIZED ORDER>, ...]
        },
        {
            "id": 2,
            "username": "kevin",
            "balance": 10,
            "cart": [<SERIALIZED CART>],
            "orders": [<SERIALIZED ORDER>, ...]
        }
        ...
    ]
}
```

## Get Buyer by ID

[GET] /api/buyers/<int:buyer_id>/

Response:

```json
{
    "success": true,
    "data": {
        "id": <ID>,
        "username": <USERNAME>,
        "balance": <BALANCE>,
        "cart": [<SERIALIZED CART>],
        "orders": [<SERIALIZED ORDER>, ...]
    }
}
```

## Delete Buyer

[DELETE] /api/buyers/<int:buyer_id>/

Response:

```json
{
    "success": true,
    "data": {
        "id": <ID>,
        "username": <USERNAME>,
        "balance": <BALANCE>,
        "cart": [<SERIALIZED CART>],
        "orders": [<SERIALIZED ORDER>,...]
    }
}
```

## Add to Cart

[POST] /api/buyers/<int:buyer_id>/add/

Request:

```json
{
	"item_id": <USER INPUT>
}
```

Response:

```json
{
    "success": true,
    "data": {
        "id": <BUYER_ID>,
        "total": <UPDATED TOTAL PRICE OF CART>,
        "items": [
            {
                "id": <USER INPUT FOR ITEM_ID>,
                "name": <NAME>,
                "price": <PRICE>
            },
            ...
        ]
    }
}
```

## Remove from Cart

[POST] /api/buyers/<int:buyer_id>/remove/

Request:

```json
{
	"item_id": <USER INPUT>
}
```

Response:

```json
{
    "success": true,
    "data": {
        "id": <USER INPUT FOR ID>,
        "total": <UPDATED TOTAL>,
        "items": <SERIALILIZED ITEM LIST WITH SPECIFIED ITEM REMOVED>
    }
}
```

## Checkout Cart

[POST] /api/buyers/<int:buyer_id>/checkout/

Response:

```json
{
    "success": true,
    "data": {
        "id": <BUYER_ID>,
        "username": <USERNAME>,
        "balance": <UPDATED BALANCE>,
        "cart": [
            {
                "total": 0,
                "items": []
            }
        ],
        "orders": [<SERIALIZED ORDER LIST WITH CART ITEMS ADDED AS AN ORDER>]
    }
}
```






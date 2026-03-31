# 🧩 Complete cJSON Function Reference (ESP32 / ESP-IDF)

This document explains **all major cJSON functions used in this
project**, in a **step-by-step workflow**:

> 🟢 Create JSON → 🟡 Modify → 🔵 Parse → 🔴 Cleanup

------------------------------------------------------------------------

# 🟢 1. JSON CREATION FUNCTIONS

## 🔹 cJSON_CreateObject()

Creates a root JSON object.

``` c
cJSON *root = cJSON_CreateObject();
```

## 🔹 cJSON_AddStringToObject()

``` c
cJSON_AddStringToObject(root, "device", "ESP32");
```

## 🔹 cJSON_AddNumberToObject()

``` c
cJSON_AddNumberToObject(root, "uptime_sec", 12345);
```

## 🔹 cJSON_AddBoolToObject()

``` c
cJSON_AddBoolToObject(root, "connected", true);
```

## 🔹 cJSON_AddNullToObject()

``` c
cJSON_AddNullToObject(root, "error");
```

## 🔹 cJSON_AddArrayToObject()

``` c
cJSON *features = cJSON_AddArrayToObject(root, "features");
```

## 🔹 cJSON_CreateString()

``` c
cJSON *str = cJSON_CreateString("WiFi");
```

## 🔹 cJSON_AddItemToArray()

``` c
cJSON_AddItemToArray(features, cJSON_CreateString("WiFi"));
cJSON_AddItemToArray(features, cJSON_CreateString("BLE"));
```

## 🔹 cJSON_InsertItemInArray()

``` c
cJSON_InsertItemInArray(features, 1, cJSON_CreateString("OTA"));
```

## 🔹 cJSON_AddObjectToObject()

``` c
cJSON *config = cJSON_AddObjectToObject(root, "config");
cJSON_AddNumberToObject(config, "cpu_mhz", 240);
cJSON_AddStringToObject(config, "flash", "4MB");
```

------------------------------------------------------------------------

# 🟡 2. JSON SERIALIZATION

## 🔹 cJSON_PrintUnformatted()

``` c
char *json_str = cJSON_PrintUnformatted(root);
```

## 🔹 cJSON_Print()

``` c
char *pretty = cJSON_Print(root);
```

------------------------------------------------------------------------

# 🔵 3. JSON PARSING FUNCTIONS

## 🔹 cJSON_ParseWithOpts()

``` c
cJSON *root = cJSON_ParseWithOpts(json_str, NULL, 1);
```

## 🔹 cJSON_GetObjectItemCaseSensitive()

``` c
cJSON *device = cJSON_GetObjectItemCaseSensitive(root, "device");
```

## 🔹 Type Checking

``` c
cJSON_IsString(device);
cJSON_IsNumber(item);
cJSON_IsBool(item);
cJSON_IsNull(item);
cJSON_IsArray(item);
cJSON_IsObject(item);
```

## 🔹 cJSON_GetObjectItem()

``` c
cJSON *features = cJSON_GetObjectItem(root, "features");
```

## 🔹 cJSON_ArrayForEach()

``` c
cJSON *item = NULL;
cJSON_ArrayForEach(item, features)
{
    if (cJSON_IsString(item))
    {
        printf("%s\n", item->valuestring);
    }
}
```

------------------------------------------------------------------------

# 🟠 4. JSON MODIFICATION FUNCTIONS

## 🔹 cJSON_ReplaceItemInObject()

``` c
cJSON_ReplaceItemInObject(root, "device",
                         cJSON_CreateString("ESP32-S3"));
```

## 🔹 cJSON_DetachItemFromObject()

``` c
cJSON *detached = cJSON_DetachItemFromObject(root, "error");
cJSON_Delete(detached);
```

## 🔹 Add New Field

``` c
cJSON_AddStringToObject(root, "status", "running");
```

## 🔹 cJSON_Duplicate()

``` c
cJSON *copy = cJSON_Duplicate(root, 1);
```

## 🔹 cJSON_Compare()

``` c
if (cJSON_Compare(root, copy, 1))
{
    printf("Match\n");
}
```

------------------------------------------------------------------------

# 🔴 5. MEMORY MANAGEMENT

## 🔹 cJSON_Delete()

``` c
cJSON_Delete(root);
```

## 🔹 free()

``` c
free(json_str);
free(pretty);
```

------------------------------------------------------------------------

# 🔄 FULL FLOW EXAMPLE

``` c
cJSON *root = cJSON_CreateObject();
cJSON_AddStringToObject(root, "device", "ESP32");

char *json = cJSON_PrintUnformatted(root);

cJSON *parsed = cJSON_Parse(json);

cJSON *dev = cJSON_GetObjectItem(parsed, "device");

cJSON_ReplaceItemInObject(parsed, "device",
                         cJSON_CreateString("ESP32-S3"));

free(json);
cJSON_Delete(parsed);
cJSON_Delete(root);
```

------------------------------------------------------------------------

# ⚠️ RULES

-   Always check types
-   Always free memory
-   Avoid leaks

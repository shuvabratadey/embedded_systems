#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "cJSON_Utils.h"

int main()
{
    printf("=== cJSON ADVANCED TUTORIAL ===\n\n");

    /* =====================================================
       1. CREATE ROOT OBJECT
    ====================================================== */
    cJSON *root = cJSON_CreateObject();

    /* =====================================================
       2. ADD BASIC TYPES
    ====================================================== */
    cJSON_AddStringToObject(root, "name", "Shuva");
    cJSON_AddNumberToObject(root, "age", 25);
    cJSON_AddBoolToObject(root, "isStudent", 0);

    /* =====================================================
       3. ADD ARRAY (STRINGS)
    ====================================================== */
    cJSON *skills = cJSON_AddArrayToObject(root, "skills");

    cJSON_AddItemToArray(skills, cJSON_CreateString("C"));
    cJSON_AddItemToArray(skills, cJSON_CreateString("Embedded"));
    cJSON_AddItemToArray(skills, cJSON_CreateString("IoT"));

    /* =====================================================
       4. ADD ARRAY OF NUMBERS
    ====================================================== */
    cJSON *marks = cJSON_AddArrayToObject(root, "marks");

    cJSON_AddItemToArray(marks, cJSON_CreateNumber(85));
    cJSON_AddItemToArray(marks, cJSON_CreateNumber(90));
    cJSON_AddItemToArray(marks, cJSON_CreateNumber(95));

    /* =====================================================
       5. ADD NESTED OBJECT
    ====================================================== */
    cJSON *education = cJSON_AddObjectToObject(root, "education");

    cJSON_AddStringToObject(education, "degree", "B.Tech");
    cJSON_AddStringToObject(education, "branch", "ECE");

    /* =====================================================
       6. ARRAY OF OBJECTS (VERY IMPORTANT)
    ====================================================== */
    cJSON *projects = cJSON_AddArrayToObject(root, "projects");

    for (int i = 0; i < 2; i++)
    {
        cJSON *proj = cJSON_CreateObject();

        if (i == 0)
        {
            cJSON_AddStringToObject(proj, "title", "ESP32 Smart Watch");
            cJSON_AddNumberToObject(proj, "year", 2025);
        }
        else
        {
            cJSON_AddStringToObject(proj, "title", "IoT Automation");
            cJSON_AddNumberToObject(proj, "year", 2024);
        }

        cJSON_AddItemToArray(projects, proj);
    }

    /* =====================================================
       7. DUPLICATE & MODIFY OBJECT
    ====================================================== */
    cJSON *copy = cJSON_Duplicate(root, 1); // deep copy
    cJSON_ReplaceItemInObject(copy, "name", cJSON_CreateString("Bob"));

    /* =====================================================
       8. PRINT JSON
    ====================================================== */
    char *pretty = cJSON_Print(root);
    char *compact = cJSON_PrintUnformatted(root);

    printf("Pretty JSON:\n%s\n\n", pretty);
    printf("Compact JSON:\n%s\n\n", compact);

    /* =====================================================
       9. PARSE JSON BACK
    ====================================================== */
    cJSON *parsed = cJSON_Parse(pretty);

    if (!parsed)
    {
        printf("Parse error!\n");
        return -1;
    }

    /* =====================================================
       10. SAFE ACCESS (BEST PRACTICE)
    ====================================================== */
    cJSON *name = cJSON_GetObjectItemCaseSensitive(parsed, "name");
    if (cJSON_IsString(name))
        printf("Name: %s\n", name->valuestring);

    cJSON *age = cJSON_GetObjectItem(parsed, "age");
    if (cJSON_IsNumber(age))
        printf("Age: %d\n", age->valueint);

    cJSON *isStudent = cJSON_GetObjectItem(parsed, "isStudent");
    if (cJSON_IsBool(isStudent))
        printf("Is Student: %s\n", cJSON_IsTrue(isStudent) ? "Yes" : "No");

    /* =====================================================
       11. ITERATE ARRAY
    ====================================================== */
    cJSON *skills_arr = cJSON_GetObjectItem(parsed, "skills");

    printf("\nSkills:\n");
    cJSON *item = NULL;
    cJSON_ArrayForEach(item, skills_arr)
    {
        if (cJSON_IsString(item))
            printf(" - %s\n", item->valuestring);
    }

    /* =====================================================
       12. ITERATE ARRAY OF OBJECTS
    ====================================================== */
    cJSON *proj_arr = cJSON_GetObjectItem(parsed, "projects");

    printf("\nProjects:\n");
    cJSON_ArrayForEach(item, proj_arr)
    {
        cJSON *title = cJSON_GetObjectItem(item, "title");
        cJSON *year  = cJSON_GetObjectItem(item, "year");

        if (cJSON_IsString(title) && cJSON_IsNumber(year))
        {
            printf(" - %s (%d)\n", title->valuestring, year->valueint);
        }
    }

    /* =====================================================
       13. MODIFY JSON AFTER PARSE
    ====================================================== */
    cJSON_ReplaceItemInObject(parsed, "age", cJSON_CreateNumber(30));

    /* =====================================================
       14. DELETE ITEM
    ====================================================== */
    cJSON_DeleteItemFromObject(parsed, "marks");

    /* =====================================================
       15. PRINT MODIFIED JSON
    ====================================================== */
    char *modified = cJSON_Print(parsed);
    printf("\nModified JSON:\n%s\n\n", modified);

    /* =====================================================
       16. CLEANUP (VERY IMPORTANT)
    ====================================================== */
    free(pretty);
    free(compact);
    free(modified);

    cJSON_Delete(root);
    cJSON_Delete(copy);
    cJSON_Delete(parsed);

    printf("=== DONE ===\n");

    return 0;
}
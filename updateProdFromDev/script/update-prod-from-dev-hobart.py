'''
Truncate/Delete Rows and Append
tool for Hobart, IN features. '''

import arcpy

def replaceData(input_fc, target_fc):

    arcpy.AddMessage('Starting run...')

    input_row_count = int(arcpy.GetCount_management(input_fc)[0])

    et_switch = 0

    desc = arcpy.da.Describe(target_fc)

    if desc['editorTrackingEnabled']:

        arcpy.AddMessage('Editor tracking is enabled...')
        et_switch = 1

        arcpy.AddMessage('Identifying ET fields...')
        creator_fld = desc['creatorFieldName']
        create_date_fld = desc['createdAtFieldName']
        editor_fld = desc['editorFieldName']
        edit_date_fld= desc['editedAtFieldName']
        
        arcpy.AddMessage('Disabling editor tracking...')
        arcpy.DisableEditorTracking_management(target_fc, 'DISABLE_CREATOR', 'DISABLE_CREATION_DATE', 'DISABLE_LAST_EDITOR', 'DISABLE_LAST_EDIT_DATE')

    if desc['isVersioned']:
        
        arcpy.AddMessage('Dataset is versioned...')
        arcpy.AddMessage('Deleting rows...')
        arcpy.DeleteRows_management(target_fc)
        arcpy.AddMessage('Appending updated data...')
        arcpy.Append_management(input_fc, target_fc, 'NO_TEST')

        if et_switch == 1:
            
            arcpy.AddMessage('Enabling editor tacking...')
            arcpy.EnableEditorTracking_management(target_fc, creator_fld, create_date_fld, editor_fld, edit_date_fld, 'NO_ADD_FIELDS')
            
    else:

        arcpy.AddMessage('Truncating dataset...')
        arcpy.TruncateTable_management(target_fc)
        arcpy.AddMessage('Appending updated data...')
        arcpy.Append_management(input_fc, target_fc, 'NO_TEST')

        if et_switch == 1:

            arcpy.AddMessage('Enabling editor tacking...')
            arcpy.EnableEditorTracking_management(target_fc, creator_fld, create_date_fld, editor_fld, edit_date_fld, 'NO_ADD_FIELDS')


    target_row_count = int(arcpy.GetCount_management(target_fc)[0])

    if input_row_count == target_row_count:

        arcpy.AddMessage('Done!')
    
    else:

        arcpy.AddWarning('Row counts from input and target do not match!')
        arcpy.AddWarning('Manual investigation is required!')
        arcpy.AddWarning('Compare field lengths and types to ensure the schemas match.')

if __name__ == '__main__':

    dev_fc = arcpy.GetParameterAsText(0)
    prod_fc = arcpy.GetParameterAsText(1)

    try:

        replaceData(dev_fc, prod_fc)

    except Exception as e:

        arcpy.AddWarning(e)
        arcpy.AddError('Run failed :(')


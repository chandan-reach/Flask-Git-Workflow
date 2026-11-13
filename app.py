@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():

    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return "To-Do item saved successfully!"
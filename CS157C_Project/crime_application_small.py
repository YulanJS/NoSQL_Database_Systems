# ----------------------------------------------------------------------
# Name:       crime_application
# Purpose:    Use a MongoDB database to analyze Chicago Crime Information
#
# Date:       Spring 2019
# ----------------------------------------------------------------------
import tkinter
from pymongo import MongoClient
from bson.son import SON
from pymongo.errors import ConnectionFailure


class Analyzer:
    """
    Create the gui for the application and run it

    Arguments:
        parent: The root tkinter.tk object
        client: The pymongo MongoClient
    """

    def __init__(self, parent, client):
        parent.title('Chicago Crime Analyzer')
        self.parent = parent
        self.client = client

        #  Connect to db and choose collection
        self.db_name = 'small_db'
        self.database = client[self.db_name]
        self.collection = self.database['crimes']

        #  Create fields and labels
        case_num_label = tkinter.Label(parent, text="CASE#: ")
        case_num_label.grid(row=0, column=0)
        self.case_num_prompt = tkinter.Entry(parent, width=20)
        self.case_num_prompt.grid(row=0, column=1, columnspan=2,
                                  sticky='w')

        date_label = tkinter.Label(parent, text="DATE: ")
        date_label.grid(row=1, column=0)
        self.date_prompt = tkinter.Entry(parent, width=20)
        self.date_prompt.grid(row=1, column=1, columnspan=2,
                              sticky='w')

        block_label = tkinter.Label(parent, text="BLOCK: ")
        block_label.grid(row=2, column=0)
        self.block_prompt = tkinter.Entry(parent, width=20)
        self.block_prompt.grid(row=2, column=1, columnspan=2,
                               sticky='w')

        iucr_label = tkinter.Label(parent, text="IUCR")
        iucr_label .grid(row=3, column=0)
        self.iucr_prompt = tkinter.Entry(parent)
        self.iucr_prompt.grid(row=3, column=1, columnspan=2,
                              sticky='w')

        primary_description_label = tkinter.Label(parent, text="PRIMARY "
                                                  "DESCRIPTION: ")
        primary_description_label.grid(row=4, column=0)
        self.primary_description_prompt = tkinter.Entry(parent)
        self.primary_description_prompt.grid(row=4, column=1, columnspan=2,
                                             sticky='w')

        arrest_label = tkinter.Label(parent, text="ARREST: ")
        arrest_label.grid(row=5, column=0)
        self.arrest_prompt = tkinter.Entry(parent)
        self.arrest_prompt.grid(row=5, column=1, columnspan=2,
                                sticky='w')

        domestic_label = tkinter.Label(parent, text="DOMESTIC: ")
        domestic_label.grid(row=6, column=0)
        self.domestic_prompt = tkinter.Entry(parent)
        self.domestic_prompt.grid(row=6, column=1, columnspan=2,
                                  sticky='w')

        district_label = tkinter.Label(parent, text="DISTRICT: ")
        district_label.grid(row=7, column=0)
        self.district_prompt = tkinter.Entry(parent)
        self.district_prompt.grid(row=7, column=1, columnspan=2,
                                  sticky='w')

        ward_label = tkinter.Label(parent, text="WARD: ")
        ward_label.grid(row=8, column=0)
        self.ward_prompt = tkinter.Entry(parent)
        self.ward_prompt.grid(row=8, column=1, columnspan=2,
                              sticky='w')

        year_label = tkinter.Label(parent, text="YEAR: ")
        year_label.grid(row=9, column=0)
        self.year_prompt = tkinter.Entry(parent, width=20)
        self.year_prompt.grid(row=9, column=1, columnspan=2,
                              sticky='w')

        date_label = tkinter.Label(parent, text="DATE: ")
        date_label.grid(row=9, column=0)
        self.date_prompt = tkinter.Entry(parent, width=20)
        self.date_prompt.grid(row=9, column=1, columnspan=2,
                              sticky='w')

        #  Create buttons for functions
        self.current_buttons = []

        #  Find menu
        self.find_menu_button = \
            tkinter.Button(parent, text="Find a document ", width=25,
                           command=self.enter_find_menu, bg="#FFE6A8")
        self.find_menu_button.grid(row=0, column=3)

        self.find_button = tkinter.Button(parent, text="Find document",
                                          width=25, command=self.find_document)
        self.find_button.grid(row=0, column=4)
        self.current_buttons.append(self.find_button)

        self.get_crime_counts_button = \
            tkinter.Button(parent, text="Count Each Type of Crime",
                           width=25, command=self.count_crime_types)
        self.get_crime_counts_button.grid(row=1, column=4)
        self.current_buttons.append(self.get_crime_counts_button)

        self.get_most_common_crime_button = \
            tkinter.Button(parent, text="Get Most Common Type of Crime",
                           width=25, command=self.get_most_common_crime)
        self.get_most_common_crime_button.grid(row=2, column=4)
        self.current_buttons.append(self.get_most_common_crime_button)

        self.get_domestic_crimes_with_arrest_button = \
            tkinter.Button(parent, text="Get Domestic Crimes With Arrest",
                           width=25,
                           command=self.get_domestic_crimes_with_arrest)
        self.get_domestic_crimes_with_arrest_button.grid(row=3, column=4)
        self.current_buttons.append(
            self.get_domestic_crimes_with_arrest_button)

        #  Insert menu
        self.insert_menu_button = \
            tkinter.Button(parent, text="Insert a document ", width=25,
                           command=self.enter_insert_menu, bg="#FFE6A8")
        self.insert_menu_button.grid(row=1, column=3)
        self.insert_button = tkinter.Button(parent, text="Insert Data",
                                            width=25,
                                            command=self.insert_data)

        #  Update Menu
        self.update_menu_button = \
            tkinter.Button(parent, text="Update a document ", width=25,
                           command=self.enter_update_menu, bg="#FFE6A8")
        self.update_menu_button.grid(row=2, column=3)

        self.select_for_update_button = \
            tkinter.Button(parent, text="Select documents to update",
                           width=25, command=self.select_documents_to_update)

        self.update_selected_documents_button = \
            tkinter.Button(parent, text="Update Selected Documents",
                           width=25, command=self.update_selected_documents)

        self.documents_selected = False

        #  Delete Menu
        self.delete_menu_button = \
            tkinter.Button(parent, text="Delete a document ", width=25,
                           command=self.enter_delete_menu, bg="#FFE6A8")
        self.delete_menu_button.grid(row=3, column=3)

        self.delete_button = tkinter.Button(parent, text="Delete Data",
                                            width=25,
                                            command=self.delete_data)

        #  Status and Result display
        self.status_display = tkinter.Label(parent, text="Crime Application")
        self.status_display.grid(row=6, rowspan=2, column=3, columnspan=2)

        self.result_display = tkinter.Listbox(parent, width=70, height=15)
        self.result_display.grid(row=0, rowspan=10, column=5, sticky='n')
        self.result_display.insert('end', "Results Here")

        h_scrollbar = tkinter.Scrollbar(parent, orient="horizontal")
        h_scrollbar.grid(column=5, sticky='we')
        h_scrollbar.config(command=self.result_display.xview)

        v_scrollbar = tkinter.Scrollbar(parent, orient="vertical")
        v_scrollbar.grid(row=0, rowspan=10, column=6, sticky='ns')
        v_scrollbar.config(command=self.result_display.yview)

        self.result_display.config(xscrollcommand=h_scrollbar.set)
        self.result_display.config(yscrollcommand=v_scrollbar.set)

    def enter_find_menu(self):
        """
        Clear the menu of its current buttons and show the find
        document buttons

        :return: None
        """
        for btn in self.current_buttons:
            btn.grid_forget()
        self.current_buttons.clear()

        self.find_button.grid(row=0, column=4)
        self.current_buttons.append(self.find_button)

        self.get_crime_counts_button.grid(row=1, column=4)
        self.current_buttons.append(self.get_crime_counts_button)

        self.get_most_common_crime_button.grid(row=2, column=4)
        self.current_buttons.append(self.get_most_common_crime_button)

        self.get_domestic_crimes_with_arrest_button.grid(row=3, column=4)
        self.current_buttons.append(
            self.get_domestic_crimes_with_arrest_button)

    def enter_update_menu(self):
        """
        Clear the menu of its current buttons and show the update
        document buttons

        :return: None
        """
        for btn in self.current_buttons:
            btn.grid_forget()
        self.current_buttons.clear()

        self.select_for_update_button.grid(row=0, column=4)
        self.current_buttons.append(self.select_for_update_button)

        self.update_selected_documents_button.grid(row=1, column=4)
        self.current_buttons.append(self.update_selected_documents_button)

    def enter_insert_menu(self):
        """
        Clear the menu of its current buttons and show the insert
        document buttons

        :return: None
        """
        for btn in self.current_buttons:
            btn.grid_forget()
        self.current_buttons.clear()

        self.insert_button.grid(row=0, column=4)
        self.current_buttons.append(self.insert_button)

    def enter_delete_menu(self):
        """
        Clear the menu of its current buttons and show the delete
        document buttons

        :return: None
        """
        for btn in self.current_buttons:
            btn.grid_forget()
        self.current_buttons.clear()

        self.delete_button.grid(row=0, column=4)
        self.current_buttons.append(self.delete_button)

    def find_document(self):
        """
        Get the document information from the entry widgets and call
        db.collection.find(document_to_find) to find the documents
        specified. Limited to showing first 30 documents found.

        :return: None
        """
        self.status_display.configure(text="Running")
        document_to_find = self.get_document_from_prompts()
        self.result_display.delete(0, 'end')
        try:
            count = 0
            for found_document in self.collection.find(
                    document_to_find).limit(30):
                self.result_display.insert('end', str(found_document))
                count += 1
            if count == 30:
                limit_reached_text = "Limit on documents to find reached (" \
                                     "limit = 30)"
                self.result_display.insert('end', limit_reached_text)
                # print("Limit on documents to find reached (limit = 30)")
            if count == 0:
                self.result_display.insert('end', 'No Documents Found')
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Documents Found")

    def insert_data(self):
        """
        Get the document information from the entry widgets and insert
        a document containing that data into the collection.

        :return: None
        """
        self.status_display.configure(text="Running")
        document_to_insert = self.get_document_from_prompts()
        self.collection.insert_one(document_to_insert)
        self.status_display.configure(text="Insert Complete")

    def select_documents_to_update(self):
        """
        Get the document information from the entry widgets and select
        those documents to be updated. Documents will not be updated
        until update_selected_documents() is called.

        :return: None
        """
        self.status_display.configure(text="Running")
        self.documents_to_update = self.get_document_from_prompts()
        self.status_display.configure(text="Documents to update found. "
                                           "Enter in new values")
        self.documents_selected = True

    def update_selected_documents(self):
        """
        Get the document information from the entry widgets and update
        all selected documents with the new information. Does nothing if
        no documents have been selected yet.

        :return: None
        """
        # myquery = {"address": "Valley 345"}
        # newvalues = {"$set": {"address": "Canyon 123"}}
        # self.collection.update_one(myquery, newvalues)
        if self.documents_selected:
            self.status_display.configure(text="Running")
            new_values = self.get_document_from_prompts()
            new_values = {"$set": new_values}
            self.collection.update_many(self.documents_to_update, new_values)
            result_string = f'Documents Updated'
            self.status_display.configure(text=result_string)
        else:
            self.status_display.configure(text="No documents have been "
                                               "selected")

    def delete_data(self):
        """
        Get the document information from the entry widgets and delete
        those documents from the database.

        :return: None
        """
        self.status_display.configure(text="Running")
        documents_to_delete = self.get_document_from_prompts()
        self.collection.delete_many(documents_to_delete)
        result_string = f'Delete Complete'
        self.status_display.configure(text=result_string)

    def get_document_from_prompts(self):
        """
        Read all of the entry widgets. If they are not empty, then add
        the corresponding information to the dictionary. The dictionary
        represents the document in MongoDB.

        :return: document: (Dictionary) A dictionary representing a
        JSON document in MongoDB.
        """
        case_num = self.case_num_prompt.get()
        date = ""
        block = self.block_prompt.get()
        iucr = self.iucr_prompt.get()
        primary_description = self.primary_description_prompt.get()
        arrest = self.arrest_prompt.get()
        domestic = self.domestic_prompt.get()
        district = "" # self.district_prompt.get()
        ward = self.ward_prompt.get()
        year = "" # self.year_prompt.get()
        updated_on = ""
        document = {}
        if case_num != "":
            document["CASE#"] = case_num.upper()
        if date != "":
            document["DATE"] = date
        if block != "":
            document["BLOCK"] = block.upper()
        if iucr != "":
            document["IUCR"] = iucr
        if primary_description != "":
            document["PRIMARY DESCRIPTION"] = primary_description.upper()
        if arrest != "":
            document["ARREST"] = arrest.upper()
        if domestic != "":
            document["DOMESTIC"] = domestic.upper()
        if district != "":
            document["DISTRICT"] = district.upper()
        if ward != "":
            try:
                document["WARD"] = int(ward)
            except ValueError:
                pass
        if year != "":
            try:
                document["YEAR"] = int(year)
            except ValueError:
                pass
        if updated_on != "":
            document["UPDATED ON"] = updated_on
        print(document)
        return document

    def count_crime_types(self):
        try:
            pipeline = [
                {"$group": {"_id": {"type": "$PRIMARY DESCRIPTION"}, "total": {
                 "$sum": 1}}},
                {"$sort": SON([("total", -1)])}
            ]

            count = 0
            self.result_display.delete(0, 'end')

            for found_counts in self.collection.aggregate(pipeline):
                self.result_display.insert('end', str(found_counts))
                count += 1
            if count == 30:
                limit_reached_text = "Limit on documents to find reached (" \
                                     "limit = 30)"
                self.result_display.insert('end', limit_reached_text)
                # print("Limit on documents to find reached (limit = 30)")
            if count == 0:
                self.result_display.insert('end', 'No Documents Found')
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Document Found")

    def get_most_common_crime(self):
        """
        Find and display the most common type of crime by counting
        the number of each type of crime and displaying the top one

        :return: None
        """
        try:
            pipeline = [
                {"$group": {"_id": {"type": "$PRIMARY DESCRIPTION"}, "total": {
                 "$sum": 1}}},
                {"$sort": SON([("total", -1)])},
                {"$limit": 1}
            ]
            found_document = self.collection.aggregate(pipeline)

            self.result_display.delete(0, 'end')
            if not found_document:
                self.result_display.insert('end', 'No Documents Found')
            else:
                for found_count in found_document:
                    self.result_display.insert('end', str(found_count))
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Document Found")

    def get_domestic_crimes_with_arrest(self):
        """
        Find Crimes where the Crime was Domestics and where
        an Arrest was made

        :return: None
        """
        self.status_display.configure(text="Running")
        document_to_find = {"ARREST": "Y", "DOMESTIC": "Y"}
        self.result_display.delete(0, 'end')
        try:
            count = 0
            for found_document in self.collection.find(
                    document_to_find).limit(30):
                self.result_display.insert('end', str(found_document))
                count += 1
            if count == 30:
                limit_reached_text = "Limit on documents to find reached (" \
                                     "limit = 30)"
                self.result_display.insert('end', limit_reached_text)
                # print("Limit on documents to find reached (limit = 30)")
            if count == 0:
                self.result_display.insert('end', 'No Documents Found')
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Documents Found")


def main():
    client = MongoClient('mongodb://localhost:27017/')

    # Test if the connection is successful
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server not available")

    root = tkinter.Tk()
    analyzer = Analyzer(root, client)
    root.mainloop()


if __name__ == '__main__':
    main()

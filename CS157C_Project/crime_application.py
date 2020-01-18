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
        self.db_name = 'test_db'
        self.database = client[self.db_name]
        self.collection = self.database['crimes']

        #  Create fields and labels
        case_num_label = tkinter.Label(parent, text="Case Number: ")
        case_num_label.grid(row=0, column=0)
        self.case_num_prompt = tkinter.Entry(parent, width=20)
        self.case_num_prompt.grid(row=0, column=1, columnspan=2,
                                  sticky='w')

        date_label = tkinter.Label(parent, text="Date: ")
        date_label.grid(row=1, column=0)
        self.date_prompt = tkinter.Entry(parent, width=20)
        self.date_prompt.grid(row=1, column=1, columnspan=2,
                              sticky='w')

        block_label = tkinter.Label(parent, text="Block: ")
        block_label.grid(row=2, column=0)
        self.block_prompt = tkinter.Entry(parent, width=20)
        self.block_prompt.grid(row=2, column=1, columnspan=2,
                               sticky='w')

        iucr_label = tkinter.Label(parent, text="IUCR")
        iucr_label .grid(row=3, column=0)
        self.iucr_prompt = tkinter.Entry(parent)
        self.iucr_prompt.grid(row=3, column=1, columnspan=2,
                              sticky='w')

        primary_type_label = tkinter.Label(parent, text="Primary Type: ")
        primary_type_label.grid(row=4, column=0)
        self.primary_type_prompt = tkinter.Entry(parent)
        self.primary_type_prompt.grid(row=4, column=1, columnspan=2,
                                      sticky='w')

        arrest_label = tkinter.Label(parent, text="Arrest: ")
        arrest_label.grid(row=5, column=0)
        self.arrest_prompt = tkinter.Entry(parent)
        self.arrest_prompt.grid(row=5, column=1, columnspan=2,
                                sticky='w')

        domestic_label = tkinter.Label(parent, text="Domestic: ")
        domestic_label.grid(row=6, column=0)
        self.domestic_prompt = tkinter.Entry(parent)
        self.domestic_prompt.grid(row=6, column=1, columnspan=2,
                                  sticky='w')

        district_label = tkinter.Label(parent, text="District: ")
        district_label.grid(row=7, column=0)
        self.district_prompt = tkinter.Entry(parent)
        self.district_prompt.grid(row=7, column=1, columnspan=2,
                                  sticky='w')

        ward_label = tkinter.Label(parent, text="Ward: ")
        ward_label.grid(row=8, column=0)
        self.ward_prompt = tkinter.Entry(parent)
        self.ward_prompt.grid(row=8, column=1, columnspan=2,
                              sticky='w')

        year_label = tkinter.Label(parent, text="Year: ")
        year_label.grid(row=9, column=0)
        self.year_prompt = tkinter.Entry(parent, width=20)
        self.year_prompt.grid(row=9, column=1, columnspan=2,
                              sticky='w')

        updated_on_label = tkinter.Label(parent, text="Updated On: ")
        updated_on_label.grid(row=10, column=0)
        self.updated_on_prompt = tkinter.Entry(parent, width=20)
        self.updated_on_prompt.grid(row=10, column=1, columnspan=2,
                                    sticky='w')

        #  Create buttons for functions
        self.current_buttons = []

        #  Find menu
        self.find_menu_button = \
            tkinter.Button(parent, text="Find a document ", width=25,
                           command=self.enter_find_menu, bg="#FFE6A8")
        self.find_menu_button.grid(row=0, column=3)

        self.find_button = tkinter.Button(parent, text="Find "
                                                       "Specified Document",
                                          width=25, command=self.find_document)
        self.find_button.grid(row=0, column=4)
        self.current_buttons.append(self.find_button)

        self.find_on_specific_date_button = \
            tkinter.Button(parent, text="Find Reports On Specific Date",
                           width=25,
                           command=self.find_on_specific_date)
        self.find_on_specific_date_button.grid(row=1, column=4)
        self.current_buttons.append(
            self.find_on_specific_date_button)

        self.find_last_updated_on_button = \
            tkinter.Button(parent, text="Find Reports Last Updated On",
                           width=25,
                           command=self.find_last_updated_on)
        self.find_last_updated_on_button.grid(row=2, column=4)
        self.current_buttons.append(
            self.find_last_updated_on_button)

        self.get_domestic_crimes_with_arrest_button = \
            tkinter.Button(parent, text="Get Domestic Crimes With Arrest",
                           width=25,
                           command=self.get_domestic_crimes_with_arrest)
        self.get_domestic_crimes_with_arrest_button.grid(row=3, column=4)
        self.current_buttons.append(
            self.get_domestic_crimes_with_arrest_button)

        self.get_start_year_button = \
            tkinter.Button(parent, text="Get Start Year For Range",
                           width=25, command=self.get_start_year)
        self.get_start_year_button.grid(row=4, column=4)
        self.current_buttons.append(self.get_start_year_button)

        self.start_year = 2001

        self.total_year_range_button = \
            tkinter.Button(parent, text="Total Reports To Year Range",
                           width=25, command=self.total_year_range)
        self.total_year_range_button.grid(row=5, column=4)
        self.current_buttons.append(self.total_year_range_button)

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

        #  Analytics Menu
        self.analytics_menu_button = \
            tkinter.Button(parent, text="Crime Analytics", width=25,
                           command=self.enter_analytics_menu, bg="#FFE6A8")
        self.analytics_menu_button.grid(row=4, column=3)

        self.get_total_reports_button = \
            tkinter.Button(parent, text="Get Total Reports", width=25,
                           command=self.get_total_reports)

        self.get_year_max_reports_button = \
            tkinter.Button(parent, text="Get Year With Most Reports",
                           width=25, command=self.get_year_max_reports)

        self.get_year_min_reports_button = \
            tkinter.Button(parent, text="Get Year With Least Reports",
                           width=25, command=self.get_year_min_reports)

        self.get_most_dangerous_block_button = \
            tkinter.Button(parent, text="Get Most Dangerous Block", width=25,
                           command=self.get_most_dangerous_block)

        self.get_total_reports_on_specific_date = \
            tkinter.Button(parent, text="Get Total Reports On Specific Date",
                           width=25,
                           command=self.get_total_reports_on_specific_date)

        self.get_crime_counts_button = \
            tkinter.Button(parent, text="Count Each Type of Crime",
                           width=25, command=self.count_crime_types)

        self.get_most_common_crime_button = \
            tkinter.Button(parent, text="Get Most Common Type of Crime",
                           width=25, command=self.get_most_common_crime)

        #  Status and Result display
        self.status_display = tkinter.Label(parent, text="Crime Application")
        self.status_display.grid(row=8, rowspan=2, column=3, columnspan=2)

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

        self.find_on_specific_date_button.grid(row=1, column=4)
        self.current_buttons.append(
            self.find_on_specific_date_button)

        self.find_last_updated_on_button.grid(row=2, column=4)
        self.current_buttons.append(
            self.find_last_updated_on_button)

        self.get_domestic_crimes_with_arrest_button.grid(row=3, column=4)
        self.current_buttons.append(
            self.get_domestic_crimes_with_arrest_button)

        self.get_start_year_button.grid(row=4, column=4)
        self.current_buttons.append(self.get_start_year_button)

        self.total_year_range_button.grid(row=5, column=4)
        self.current_buttons.append(self.total_year_range_button)

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

    def enter_analytics_menu(self):
        """
        Clear the menu of its current buttons and show the crime
        analytics buttons

        :return: None
        """
        for btn in self.current_buttons:
            btn.grid_forget()
        self.current_buttons.clear()

        self.get_total_reports_button.grid(row=0, column=4)
        self.current_buttons.append(self.get_total_reports_button)

        self.get_year_max_reports_button.grid(row=1, column=4)
        self.current_buttons.append(self.get_year_max_reports_button)

        self.get_year_min_reports_button.grid(row=2, column=4)
        self.current_buttons.append(self.get_year_min_reports_button)

        self.get_most_dangerous_block_button.grid(row=3, column=4)
        self.current_buttons.append(self.get_most_dangerous_block_button)

        self.get_total_reports_on_specific_date.grid(row=4, column=4)
        self.current_buttons.append(self.get_total_reports_on_specific_date)

        self.get_crime_counts_button.grid(row=5, column=4)
        self.current_buttons.append(self.get_crime_counts_button)

        self.get_most_common_crime_button.grid(row=6, column=4)
        self.current_buttons.append(self.get_most_common_crime_button)

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
        date = self.date_prompt.get()
        block = self.block_prompt.get()
        iucr = self.iucr_prompt.get()
        primary_type = self.primary_type_prompt.get()
        arrest = self.arrest_prompt.get()
        domestic = self.domestic_prompt.get()
        district = self.district_prompt.get()
        ward = self.ward_prompt.get()
        year = self.year_prompt.get()
        updated_on = self.updated_on_prompt.get()
        document = {}
        if case_num != "":
            document["Case Number"] = case_num.upper()
        if date != "":
            document["Date"] = date
        if block != "":
            document["Block"] = block.upper()
        if iucr != "":
            try:
                document["IUCR"] = int(iucr)
            except ValueError:
                pass
        if primary_type != "":
            document["Primary Type"] = primary_type.upper()
        if arrest != "":
            document["Arrest"] = arrest
        if domestic != "":
            document["Domestic"] = domestic
        if district != "":
            try:
                document["District"] = int(district)
            except ValueError:
                pass
        if ward != "":
            try:
                document["Ward"] = int(ward)
            except ValueError:
                pass
        if year != "":
            try:
                document["Year"] = int(year)
            except ValueError:
                pass
        if updated_on != "":
            document["Updated On"] = updated_on
        print(document)
        return document

    def count_crime_types(self):
        try:
            pipeline = [
                {"$group": {"_id": {"Type": "$Primary Type"}, "total": {
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
            self.status_display.configure(text="Documents Found")

    def get_most_common_crime(self):
        """
        Find and display the most common type of crime by counting
        the number of each type of crime and displaying the top one

        :return: None
        """
        try:
            pipeline = [
                {"$group": {"_id": {"Type": "$Primary Type"}, "total": {
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
        document_to_find = {"Arrest": "true", "Domestic": "true"}
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

    def find_on_specific_date(self):
        """
        Find documents on a specific date.
        :return:
        """
        self.status_display.configure(text="Running")

        date = self.get_document_from_prompts()

        # End early if no date found
        # date is a dictionary, it may not contain the key Date
        # use not in to check for keys
        if "Date" not in date:
            self.status_display.configure(text="No Date Specified")
            return None

        # Retrieve just the date part of the Date column (not time)
        date = date["Date"]

        document_to_find = {"Date": {"$regex": date}}
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
                self.result_display.insert('end', 'Try seeing if your format '
                                                  'is correct')
                text = f'Date Format is: (mm/dd/yyyy) (hh:mm:ss)(AM/PM)'
                self.result_display.insert('end', text)
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Documents Found")

    def find_last_updated_on(self):
        """
        Find documents on a last updated on a specific date.

        :return:None
        """
        self.status_display.configure(text="Running")

        date = self.get_document_from_prompts()

        # End early if no date found
        if "Updated On" not in date:
            self.status_display.configure(text="No Date Specified")
            return None

        # Retrieve just the date part of the Date column (not time)
        date = date["Updated On"]

        document_to_find = {"Updated On": {"$regex": date}}
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
                self.result_display.insert('end', 'Try seeing if your format '
                                                  'is correct')
                text = f'Date Format is: (mm/dd/yyyy) (hh:mm:ss)(AM/PM)'
                self.result_display.insert('end', text)
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Documents Found")

    def get_total_reports(self):
        """
        Count the total document count in the collection

        :return: None
        """
        self.status_display.configure(text="Running")
        self.result_display.delete(0, 'end')
        try:
            count = self.collection.count_documents({})
            formatted_text = f'Total Number of Crimes Reported to Date: ' \
                f'{count}'
            self.result_display.insert('end', formatted_text)
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Count Found")

    def get_year_max_reports(self):
        """
        Find the year with the most number of reports

        :return: None
        """
        try:
            self.status_display.configure(text="Running")
            pipeline = [
                {"$group": {"_id": {"Year": "$Year"}, "total": {
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

    def get_year_min_reports(self):
        """
        Find the year with the least number of reports

        :return: None
        """
        try:
            self.status_display.configure(text="Running")
            pipeline = [
                {"$group": {"_id": {"Year": "$Year"}, "total": {
                 "$sum": 1}}},
                {"$sort": SON([("total", 1)])},
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

    def get_most_dangerous_block(self):
        """
        Find the most dangerous block by counting crimes in each
        block and displaying the one with the highest count

        :return: None
        """
        try:
            self.status_display.configure(text="Running")
            pipeline = [
                {"$group": {"_id": {"type": "$Block"}, "total": {
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

    def get_total_reports_on_specific_date(self):
        """
        Get the number of all reports on a specific date.
        :return:
        """
        self.status_display.configure(text="Running")

        date = self.get_document_from_prompts()
        # End early if no date found
        if "Date" not in date:
            self.status_display.configure(text="No Date Specified")
            return None
        date = date["Date"]
        document_to_find = {"Date": {"$regex": date}}
        self.result_display.delete(0, 'end')
        try:
            count = self.collection.count_documents(document_to_find)
            formatted_text = f'Total Number of Crimes Reported on Date: ' \
                f'{date} is {count}'
            self.result_display.insert('end', formatted_text)
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Count Found")

    def total_year_range(self):
        """
        Get the total number of arrests made on a specific range of
        years.

        :return: None
        """
        # End early if not start year specified
        if not self.start_year:
            self.status_display.configure(text="No Start Year Specified")
            return None

        end_year = self.get_year()
        if not end_year:
            self.status_display.configure(text="No End Year Specified")
            return None

        if self.start_year > end_year:
            self.status_display.configure(text="Start Year Cannot be greater"
                                               " than End Year")

        year_range = {"$gte": self.start_year, "$lte": end_year}
        documents_to_find = {"Year": year_range}

        self.result_display.delete(0, 'end')
        try:
            count = self.collection.count_documents(documents_to_find)
            formatted_text = f'Total Number of Crimes Reported From Year ' \
                f'{self.start_year} to {end_year}:'
            self.result_display.insert('end', formatted_text)
            self.result_display.insert('end', count)
        except Exception as e:
            print("Unexpected error:", e.__doc__)
        else:
            self.status_display.configure(text="Count Found")

    def get_start_year(self):
        """
        Set the Starting Year for the Range Function

        :return: None
        """
        self.start_year = self.get_year()
        if not self.start_year:
            self.status_display.configure(text="No Year Specified")
            return None
        else:
            text = f'Start Year Specified {self.start_year}'
            self.status_display.configure(text=text)

    def get_year(self):
        """
        Get year from the Year Prompt

        :return: (int) A year if one is in prompt, else None
        """
        year = self.year_prompt.get()
        if year != "":
            try:
                return int(year)
            except ValueError:
                pass
        return None


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

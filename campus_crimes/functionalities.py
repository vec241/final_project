'''
Varun D N - vdn207@nyu.edu
'''

'''Contains functions that handle the different functionalities'''

import handlers
import plots
import college as coll
import plottingParameters as plotting
import initial_gui as igui
import simple_gui as GUI
import GUI2
import GUI3
import GUI4
import plotting1 as plot1
import plotting2 as plot2 
import plotting3 as plot3
import plotting4 as plot4 

def get_university_crime_details_and_plot(dataframe, college_obj, crimes_obj):
	'''Computes and generates the plots for the university'''

	crime_per_student_without_average = handlers.all_crimes_per_student_over_years(college_obj, crimes_obj)	# Question 1
	crime_per_student_with_average = handlers.all_crimes_per_student_over_years(college_obj, crimes_obj, average=True)	# Question 2
	crimes_per_student_by_category = handlers.average_crimes_per_student_by_category(dataframe, 'State', crimes_obj, overall_average = True)

	pltparam = plotting.pltParam()
	answers_obj = plots.Answers(crimes_obj, college_obj, pltparam, crime_per_student_without_average, crime_per_student_with_average, crimes_per_student_by_category)

	multibar_plot = answers_obj.visualize_answer1()
	pie_chart = answers_obj.pieChart(crime_per_student_with_average)	

	return multibar_plot, pie_chart

def university_crime_explorer(dataframe, crimes_obj, university_name, branch_name, GUI_Required):
	'''Gives out the crime details related to a university + branch'''

	if GUI_Required:
		GUI.start_user_interface(dataframe)
		university_name = GUI.get_uni()
		branch_name = GUI.get_branch()

	print "Details about %s (%s) is being generated. Please wait..." % (university_name, branch_name)
	
	college_instance = handlers.college_details(dataframe, university_name, branch_name)
	college_obj = coll.College(college_instance, crimes_obj)

	multibar_plot, pie_chart = get_university_crime_details_and_plot(dataframe, college_obj, crimes_obj)
	return university_name, branch_name, multibar_plot, pie_chart

def university_comparer(dataframe, crimes_obj):
	'''Handles the functionalities of University Comparer feature'''

	GUI2.start_user_interface(dataframe)
	university_name_1 = GUI2.get_uni1()
	branch_name_1 = GUI2.get_branch1()
	university_name_2 = GUI2.get_uni2()
	branch_name_2 = GUI2.get_branch2()

	university_name_1, branch_name_1, multibar_plot_1, pie_chart_1 = university_crime_explorer(dataframe, crimes_obj, university_name_1, branch_name_1, False)
	university_name_2, branch_name_2, multibar_plot_2, pie_chart_2 = university_crime_explorer(dataframe, crimes_obj, university_name_2, branch_name_2, False)

	return multibar_plot_1, multibar_plot_2, pie_chart_1, pie_chart_2, university_name_1, branch_name_1, university_name_2, branch_name_2

def category_wise_crime(dataframe, crimes_obj):
	'''Handles the functionalities of crimes by different categories'''

	GUI3.start_user_interface(dataframe)
	category, specific_choice = GUI3.get_choices()
	crimes_per_student_by_category = handlers.average_crimes_per_student_by_category(dataframe, category, crimes_obj, overall_average = True)

	pltparam = plotting.pltParam()
	answers_obj = plots.Answers(crimes_obj, None, pltparam, None, None, None)

	bar_chart = answers_obj.simpleBarChart(crimes_per_student_by_category, specific_choice)

	return bar_chart, specific_choice

def crime_comparisons(dataframe, crimes_obj):
	'''Handles the functionalities of different crime comparisons'''

	GUI4.start_user_interface()
	crime_1, crime_2 = GUI4.get_crimes()
	crimes_per_student_state = handlers.average_crimes_per_student_by_category(dataframe, 'State', crimes_obj, overall_average = True)
	crimes_per_student_sector = handlers.average_crimes_per_student_by_category(dataframe, 'Sector_desc', crimes_obj, overall_average = True)

	pltparam = plotting.pltParam()
	answers_obj_state = plots.Answers(crimes_obj, None, pltparam, None, None, crimes_per_student_state)
	state_wide_output = answers_obj_state.visualize_answer4(crime_1, crime_2, 'State')

	answers_obj_sector = plots.Answers(crimes_obj, None, pltparam, None, None, crimes_per_student_sector)
	sector_wide_output = answers_obj_sector.visualize_answer4(crime_1, crime_2, 'Sector')

	return crime_1, crime_2, state_wide_output, sector_wide_output

def interface(dataframe, crimes_obj):
	'''Run the interace every time for the user'''

	try:

		igui.initial_gui()
		user_feature_choice = igui.get_result()

		if user_feature_choice == 1:
			university_name, branch_name, multibar_plot, pie_chart = university_crime_explorer(dataframe, crimes_obj, "", "", True)
			plot1.plotting1(multibar_plot, pie_chart, university_name, branch_name)

		elif user_feature_choice == 2:
			multibar_plot_1, multibar_plot_2, pie_chart_1, pie_chart_2, university_name_1, branch_name_1, university_name_2, branch_name_2 = university_comparer(dataframe, crimes_obj)
			plot2.plotting2(multibar_plot_1, multibar_plot_2, pie_chart_1, pie_chart_2, university_name_1, branch_name_1, university_name_2, branch_name_2)

		elif user_feature_choice == 3:
			bar_chart, specific_choice = category_wise_crime(dataframe, crimes_obj)
			plot3.plotting3(bar_chart, specific_choice)

		else:
			crime_1, crime_2, state_wide_output, sector_wide_output = crime_comparisons(dataframe, crimes_obj)
			plot4.plotting4(state_wide_output, sector_wide_output, crime_1, crime_2)

	except (NameError, KeyError):
		print "Thanks for using!"
% Data Intensive Computing: Project

% The purpose of this rresults analysis is to answer the following questions
% about serial implementation:
% > Where are the bottle necks (what takes longest to process)?
% >> Is there lots of variablity between pages and documents??


% Uneven distribution per page?

% Serial performance times for each document:
clear workspace
clear 

% Reading in & scaling the data from the pre-uploaded cvs files:
tt = readtable('results.csv');
all_results_tab = readmatrix('results.csv','NumHeaderLines', 1);
% Grouping processing times of each document page:
doc_385 = tt(strcmp(tt.File,'385.pdf'),:);
doc_386 = tt(strcmp(tt.File,'386.pdf'),:);
doc_387 = tt(strcmp(tt.File,'387.pdf'),:);
doc_388 = tt(strcmp(tt.File,'388.pdf'),:);
doc_389 = tt(strcmp(tt.File,'389.pdf'),:);
doc_390 = tt(strcmp(tt.File,'390.pdf'),:);
doc_391 = tt(strcmp(tt.File,'391.pdf'),:);

length_all_results = size(all_results_tab);

%Total times all docs:
img_time = sum(doc_385{:,3}) + sum(doc_386{:,3})+ sum(doc_387{:,3})+ sum(doc_388{:,3})+ sum(doc_389{:,3})+ sum(doc_390{:,3})+ sum(doc_391{:,3});
total_imgs = sum(doc_385{:,4}) + sum(doc_386{:,4})+ sum(doc_387{:,4})+ sum(doc_388{:,4})+ sum(doc_389{:,4})+ sum(doc_390{:,4})+ sum(doc_391{:,4});
text_time = sum(doc_385{:,5}) + sum(doc_386{:,5})+ sum(doc_387{:,5})+ sum(doc_388{:,5})+ sum(doc_389{:,5})+ sum(doc_390{:,5})+ sum(doc_391{:,5});
caption_time = sum(doc_385{:,7}) + sum(doc_386{:,7})+ sum(doc_387{:,7})+ sum(doc_388{:,7})+ sum(doc_389{:,7})+ sum(doc_390{:,7})+ sum(doc_391{:,7});
total_img_captions = sum(doc_385{:,8}) + sum(doc_386{:,8})+ sum(doc_387{:,8})+ sum(doc_388{:,8})+ sum(doc_389{:,8})+ sum(doc_390{:,8})+ sum(doc_391{:,8});
img_save_time = sum(doc_385{:,9}) + sum(doc_386{:,9})+ sum(doc_387{:,9})+ sum(doc_388{:,9})+ sum(doc_389{:,9})+ sum(doc_390{:,9})+ sum(doc_391{:,9});
number_imgs_saved = sum(doc_385{:,10}) + sum(doc_386{:,10})+ sum(doc_387{:,10})+ sum(doc_388{:,10})+ sum(doc_389{:,10})+ sum(doc_390{:,10})+ sum(doc_391{:,10});
text_save_time = sum(doc_385{:,11}) + sum(doc_386{:,11})+ sum(doc_387{:,11})+ sum(doc_388{:,11})+ sum(doc_389{:,11})+ sum(doc_390{:,11})+ sum(doc_391{:,11});

doc_process_time = img_time + text_time + caption_time; 
doc_save_time = img_save_time + text_save_time;
doc_total_time = img_time + text_time + caption_time + img_save_time + text_save_time;


% check if all images were processed:
if (total_imgs==total_img_captions)&&(total_img_captions==number_imgs_saved)&&(total_imgs==number_imgs_saved)
    good_img_process_all = "Yes";
else 
    good_img_process_all = "Nope";
end


%Plot the results:
% figure(1) % Serial Processing Times for Different Processes
% y = [img_time text_time caption_time img_save_time text_save_time];
% x = 1:1:length(y);
% 
% bar(x,y,'FaceColor',"#CC6677", 'FaceAlpha', 0.7);
% 
% ylim([0 13]);
% xticklabels(["Img Read", "Txt Read", "Caption Read", "Img Save", "Txt Save"]);
% xtickangle(45);
% 
% %# Add a text string above each bin
% for i = 1:width(x)
%     %text(['y = ', num2str(x(i))], 'VerticalAlignment', 'top', 'FontSize', 8)
%     text(i-0.4, y(i)+0.9, ['y = ', num2str(y(i)),'s'], 'VerticalAlignment', 'top', 'FontSize', 6)
% end



% figure(2)
% 
% serial_data = log([tt.ImageTime, tt.TextTime, tt.CaptionTime, tt.ImageSaveTime, tt.TextSaveTime]);
% 
% % % Changing colour scheme:
% % 
% % %colour_scheme= ["#AA7733", "#EE6677", "#CCBB44", "#228833", "#0077BB"]; %Avg, best & worst q_machines 
% % 
% % b = boxplot(serial_data);, 'Colors',colour_scheme);
% % hold on
% % for i = 1:length(colour_scheme)
% %     %b.Colors = colour_scheme(i);
% %     %b(i).BoxEdgeColor = colour_scheme(i);
% %     %b(i).BoxFaceAlpha = 0.7;
% % end
% % 
% % 
% boxplot(log([tt.ImageTime, tt.TextTime, tt.CaptionTime, tt.ImageSaveTime, tt.TextSaveTime]))
% grid on
% 
% xticklabels(["Img Read", "Txt Read", "Caption Read", "Img Save", "Txt Save"]);
% xtickangle(45);


%% 
group_labels = {'Img Read', 'Txt Read', 'Caption Read', 'Img Save', 'Txt Save'}; % x-axis labels

colors = [[0.170 0.051 0.119] [0.238 0.102 0.119] [0.204 0.187 0.068] [0.034 0.136 0.051] [0.000 0.119 0.187]];
GroupedData = [log(tt.ImageTime) log(tt.TextTime) log(tt.CaptionTime) log(tt.ImageSaveTime) log(tt.TextSaveTime)];
legendEntries = {'Img Read' 'Txt Read' 'Caption Read' 'Img Save' 'Txt Save'};


x = 1:5;

fig = figure (3);
hold on;
boxplot(GroupedData,x);

h = findobj(gca,'Tag','Box');

patch(get(h(1),'XData'),get(h(1),'YData'), [0.170 0.051 0.919],'FaceAlpha',0.3);
patch(get(h(2),'XData'),get(h(2),'YData'), [0.838 0.102 0.119],'FaceAlpha',0.3);
patch(get(h(3),'XData'),get(h(3),'YData'), [0.204 0.787 0.068],'FaceAlpha',0.3);
patch(get(h(4),'XData'),get(h(4),'YData'), [0.034 0.360 0.510],'FaceAlpha',0.3);
patch(get(h(5),'XData'),get(h(5),'YData'), [0.000 0.619 0.671],'FaceAlpha',0.3);


grid on;


% %% 
% figure(3) %Log Bar Graphs: 
% title("Serial Processing Times for Different Processes");
% bar(log([img_time, text_time, caption_time, img_save_time, text_save_time]),'FaceColor',"#CC6677", 'FaceAlpha', 0.7);
% grid on
% 
% xticklabels(["Img Read", "Txt Read", "Caption Read", "Img Save", "Txt Save"]);
% xtickangle(45);
% 
% %# Add a text string above each bin
% for i = 1:width(x)
%     %text(['y = ', num2str(x(i))], 'VerticalAlignment', 'top', 'FontSize', 8)
%     text(i-0.4, log(y(i)+3), ['y = ', num2str(y(i)),'s'], 'FontSize', 6)
% end
% 

%% Total times per doc:
% img_time_385 = sum(doc_385{:,3});
% total_imgs_385 = sum(doc_385{:,4});
% text_time_385 = sum(doc_385{:,5});
% caption_time_385 = sum(doc_385{:,7});
% total_img_captions_385 = sum(doc_385{:,8});
% img_save_time_385 = sum(doc_385{:,9});
% number_imgs_saved_385 = sum(doc_385{:,10});
% text_save_time_385 = sum(doc_385{:,11});
% 
% doc_process_time_385 = img_time_385 + text_time_385 + caption_time_385; 
% doc_save_time_385 = img_save_time_385 + text_save_time_385;
% doc_total_time_385 = img_time_385 + text_time_385 + caption_time_385 + img_save_time_385 + text_save_time_385;
% 
% % check if all images were processed:
% if (total_imgs_385==total_img_captions_385)&&(total_img_captions_385==number_imgs_saved_385)&&(total_imgs_385==number_imgs_saved_385)
%     good_img_process = "Yes";
% end

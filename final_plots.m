% Data Intensive Computing: Project graphs

% The purpose of these plots is to provide a visual aid in comparing how
% different parallelisation methods compare to serial implementations.

% The commented-out figures show:
% > Where the bottle necks in serial document processing are.
% >> If there is lots of variablity between pages and documents.
clear workspace

%% Serial Data:
% Reading in the serial data from the pre-uploaded cvs files:
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

%Total time for each doc:
doc_385_time = sum(doc_385{:,3})+sum(doc_385{:,5})+sum(doc_385{:,7})+sum(doc_385{:,9})+sum(doc_385{:,11});
doc_386_time = sum(doc_386{:,3})+sum(doc_386{:,5})+sum(doc_386{:,7})+sum(doc_386{:,9})+sum(doc_386{:,11});
doc_387_time = sum(doc_387{:,3})+sum(doc_387{:,5})+sum(doc_387{:,7})+sum(doc_387{:,9})+sum(doc_387{:,11});
doc_388_time = sum(doc_388{:,3})+sum(doc_388{:,5})+sum(doc_388{:,7})+sum(doc_388{:,9})+sum(doc_388{:,11});
doc_389_time = sum(doc_389{:,3})+sum(doc_389{:,5})+sum(doc_389{:,7})+sum(doc_389{:,9})+sum(doc_389{:,11});
doc_390_time = sum(doc_390{:,3})+sum(doc_390{:,5})+sum(doc_390{:,7})+sum(doc_390{:,9})+sum(doc_390{:,11});
doc_391_time = sum(doc_391{:,3})+sum(doc_391{:,5})+sum(doc_391{:,7})+sum(doc_391{:,9})+sum(doc_391{:,11});

serial_doc_times = [doc_385_time, doc_386_time, doc_387_time, doc_388_time, doc_389_time, doc_390_time, doc_391_time];
% check if all images were processed:
if (total_imgs==total_img_captions)&&(total_img_captions==number_imgs_saved)&&(total_imgs==number_imgs_saved)
    good_img_process_all = "Yes";
else 
    good_img_process_all = "Nope";
end

%%  Plot the serial data:
figure (1);
x = 1:5;
boxplot(log10([tt.TextTime, tt.TextSaveTime, tt.CaptionTime, tt.ImageTime, tt.ImageSaveTime]), x,"Widths", 0.8, 'Symbol','*-k');
hold on;
h = findobj(gca,'Tag','Box');
% Formatting:
patch(get(h(1),'XData'),get(h(1),'YData'), [(170/255) (51/255) (119/255)],'FaceAlpha',0.5);
patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.5);
patch(get(h(3),'XData'),get(h(3),'YData'), [(204/255) (187/255) (68/255)],'FaceAlpha',0.5);
patch(get(h(4),'XData'),get(h(4),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.5);
patch(get(h(5),'XData'),get(h(5),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.5);

%x-axis
xticklabels(["Text Read", "Text Save", "Caption Read", "Image Find", "Image Read&Save"]);
xtickangle(45);
fontname("Times New Roman");
xlabel('Job Type', "FontWeight","bold");
%legend (["Txt Save", "Img Save", "Caption Read", "Txt Read", "Img Read"], "Location","best","FontSize",10)

%y-axis
ylabel('Wall Time (s)', "FontWeight","bold");
yticklabels(["1.0e-6", "1.0e-5", "1.0e-4", "1.0e-3", "1.0e-2", "1.0e-1", "0"]);
%yticklabels([10^(-6), 10^(-5), 10^(-4), 10^(-3), 10^(-2), 10^(-1), 0]);
grid on;

%% Parallelised Data:
% Reading in the parallel data from the pre-uploaded cvs file:
            %time_t = readtable('times.csv');
jag = readtable('times_Jag.csv');
slurm = readtable('times_slurm.csv');
dica = readtable('times_dica.csv');

% Grouping processing times of each document page:
j_serial = jag(strcmp(jag.Method,'Serial'),:);
j_wrks = jag(strcmp(jag.Method,'Workers'),:);
j_scats = jag(strcmp(jag.Method,'Scatter'),:);

slurm_serial = zeros(21,1);
slurm_wrks = slurm(strcmp(slurm.Method,'Workers'),:);
slurm_scats = slurm(strcmp(slurm.Method,'Scatter'),:);

dica_serial = dica(strcmp(dica.Method,'Serial'),:);
dica_wrks = dica(strcmp(dica.Method,'Workers'),:);
dica_scats = dica(strcmp(dica.Method,'Scatter'),:);

% Matrices of each row of values:
%%% Jaguar:
jwrk_2 = j_wrks(1:21,:);
jwrk_4 = j_wrks(22:42,:);
jwrk_8 = j_wrks(43:63,:);
jwrk_16 = j_wrks(64:84,:);

jscat_2 = j_scats(1:21,:);
jscat_4 = j_scats(22:42,:);
jscat_8 = j_scats(43:63,:);
jscat_16 = j_scats(64:84,:);

%%% Slurm:
swrk_2 = slurm_wrks(1:21,:);
swrk_4 = slurm_wrks(22:42,:);
swrk_8 = slurm_wrks(43:63,:);
swrk_16 = slurm_wrks(64:84,:);

sscat_2 = slurm_scats(1:21,:);
sscat_4 = slurm_scats(22:42,:);
sscat_8 = slurm_scats(43:63,:);
sscat_16 = slurm_scats(64:84,:);

%%% Dica 10:
dwrk_2 = dica_wrks(1:21,:);
dwrk_4 = dica_wrks(22:42,:);
dwrk_8 = dica_wrks(43:63,:);
dwrk_16 = dica_wrks(64:84,:);

dscat_2 = dica_scats(1:21,:);
dscat_4 = dica_scats(22:42,:);
dscat_8 = dica_scats(43:63,:);
dscat_16 = dica_scats(64:84,:);

%% %Plot the Scatter Method results:
figure (2);
hold on;
x = 1:15;
boxplot(([j_serial.Total_Time, slurm_serial, dica_serial.Total_Time, jscat_2.Total_Time, sscat_2.Total_Time, dscat_2.Total_Time, jscat_4.Total_Time, sscat_4.Total_Time, dscat_4.Total_Time, jscat_8.Total_Time, sscat_8.Total_Time, dscat_8.Total_Time, jscat_16.Total_Time, sscat_16.Total_Time, dscat_16.Total_Time]),"Widths",0.3, 'Symbol','*-k');

h = findobj(gcf,'Tag','Box');
% Formatting:
for i=1:3:15
    patch(get(h(i),'XData'),get(h(i),'YData'), [(51/255) (34/255) (136/255)],'FaceAlpha',0.7);
    patch(get(h(i+1),'XData'),get(h(i+1),'YData'), [(17/255) (119/255) (51/255)],'FaceAlpha',0.7);
    patch(get(h(i+2),'XData'),get(h(i+2),'YData'), [(170/255) (68/255) (153/255)],'FaceAlpha',0.7);
end
% title("Scatter Method: Total")
fontname("Times New Roman");
%x-axis
xticklabels(["1 (Serial)","1 (Serial)","1 (Serial)","2","2","2","4","4","4","8","8","8","16","16","12"]);
% xtickangle(45);
xlabel('Number of Processes',"FontWeight","bold");
%y-axis
ylabel('Wall Time (s)',"FontWeight","bold");
ylim([-0.5, 13]);
legend(["Dica 10","slurm","Jaguar 1"])
grid on;
hold off

%% %Plot the Worker Method results:
figure (3);
hold on;

x = 1:15;
boxplot(([j_serial.Total_Time, slurm_serial, dica_serial.Total_Time, jwrk_2.Total_Time, swrk_2.Total_Time, dwrk_2.Total_Time, jwrk_4.Total_Time, swrk_4.Total_Time, dwrk_4.Total_Time, jwrk_8.Total_Time, swrk_8.Total_Time, dwrk_8.Total_Time, jwrk_16.Total_Time, swrk_16.Total_Time, dwrk_16.Total_Time]),"Widths",0.3, 'Symbol','*-k');

ww = findobj(gcf,'Tag','Box');
% Formatting:
for i=1:3:15
    patch(get(ww(i),'XData'),get(ww(i),'YData'), [(51/255) (187/255) (238/255)],'FaceAlpha',0.7);
    patch(get(ww(i+1),'XData'),get(ww(i+1),'YData'), [(0/255) (153/255) (136/255)],'FaceAlpha',0.7);
    patch(get(ww(i+2),'XData'),get(ww(i+2),'YData'), [(238/255) (119/255) (51/255)],'FaceAlpha',0.7);
end
title("Worker Method: Total")
fontname("Times New Roman");
%x-axis
xticklabels(['1 (Serial)','1 (Serial)','1 (Serial)',"2","2","2","4","4","4","8","8","8","16","16","12"]);
% xtickangle(45);
xlabel('Number of Processes',"FontWeight","bold");
%y-axis
ylabel('Wall Time (s)',"FontWeight","bold");
ylim([-0.5, 13]);
legend(["Dica 10","slurm","Jaguar 1"])
grid on;

% Scatter vs worker jag 1: (Best vs Serial)
figure (4)
hold on;

x = 1:15;
boxplot(([j_serial.Total_Time, jscat_2.Total_Time, jwrk_2.Total_Time, jscat_4.Total_Time, jwrk_4.Total_Time, jscat_8.Total_Time, jwrk_8.Total_Time, jscat_16.Total_Time, jwrk_16.Total_Time]),"Widths",0.3, 'Symbol','*-k');

h = findobj(gcf,'Tag','Box');
patch(get(h(9),'XData'),get(h(9),'YData'), [(85/255) (85/255) (85/255)],'FaceAlpha',0.7);
% Formatting:
for i=8:-2:0
    patch(get(h(i),'XData'),get(h(i),'YData'), [(238/255) (119/255) (51/255)],'FaceAlpha',0.7);
    patch(get(h(i+1),'XData'),get(h(i+1),'YData'), [(170/255) (68/255) (153/255)],'FaceAlpha',0.7);
end
title("Scatter vs Worker: Jaguar 1")
fontname("Times New Roman");
%x-axis
xticklabels(["1 (Serial)","2","2","4","4","8","8","16","16"]);
xtickangle(45);
xlabel('Number of Processes',"FontWeight","bold");
%y-axis
ylabel('Wall Time (s)',"FontWeight","bold");
legend(["Serial","Worker","Scatter"],'Location','north');
grid on;

%% Indiv document:
% Extract averages for each number of processes in each method
%%%% WORKER METHOD %%%%
doc_388_wkr = [
    mean(dica(strcmp(dica.File,'data/388.pdf') & strcmp(dica.Method, 'Serial'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 2 & strcmp(dica.Method, 'Workers'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 4 & strcmp(dica.Method, 'Workers'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 8 & strcmp(dica.Method, 'Workers'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 12 & strcmp(dica.Method, 'Workers'),:).Total_Time);
];
doc_389_wkr = [
    mean(dica(strcmp(dica.File,'data/389.pdf') & strcmp(dica.Method, 'Serial'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 2 & strcmp(dica.Method, 'Workers'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 4 & strcmp(dica.Method, 'Workers'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 8 & strcmp(dica.Method, 'Workers'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 12 & strcmp(dica.Method, 'Workers'),:).Total_Time);
];
%----%----%----%----%----%
%%%% SCATTER METHOD %%%%
doc_388_scat = [
    mean(dica(strcmp(dica.File,'data/388.pdf') & strcmp(dica.Method, 'Serial'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 2 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 4 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 8 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/388.pdf') & dica.Processes == 12 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
];
doc_389_scat = [
    mean(dica(strcmp(dica.File,'data/389.pdf') & strcmp(dica.Method, 'Serial'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 2 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 4 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 8 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
    mean(dica(strcmp(dica.File,'data/389.pdf') & dica.Processes == 12 & strcmp(dica.Method, 'Scatter'),:).Total_Time);
];
null_doc=[0;0;0;0;0];

%Plot the results:
figure (5)
x=1:5;
ah = axes;
%Worker
p1=bar(x,([doc_388_wkr, null_doc]),"FaceColor","#762A83", "FaceAlpha", 0.9); %Purple.
hold on
%Doc389 - Worker
p2=bar(x,([null_doc, doc_389_wkr]),"FaceColor","#AAAA00", "FaceAlpha",0.7); %Olive.
%Scatter
p3=bar(x,([doc_388_scat, null_doc]),"FaceColor","#5AAE61", "FaceAlpha",0.6); %Pastle green. 009988 -Teal
%Doc389 - Scatter
p4=bar(x,([null_doc, doc_389_scat]),"FaceColor","#A50026", "FaceAlpha",0.6); %Bright Dark Red.
grid on
xticklabels(["Serial","2","4","8","12"]);

%%Plot the first legend
lh = legend(ah, [p1(1) p2(1) p3(1) p4(1)],'Doc 388 -Worker', 'Doc 389 -Worker','Doc 388 -Scatter','Doc 389 -Scatter');
lh.Location='NorthEast';
fontname("Times New Roman");
xlabel('Number of Processes', "FontWeight","bold");
ylabel('Wall Time (s)', "FontWeight","bold");



%% As comparative bar charts: Jag vs Slurm vs Dica
% figure(9)
% x = 1:5;
% 
% % Jag:
% bar(x,([sum(j_serial{:,8})/21, (sum(jwrk_2{:,8})+sum(jscat_2{:,8}))/42, (sum(jwrk_4{:,8})+sum(jscat_4{:,8}))/42, (sum(jwrk_8{:,8})+sum(jscat_8{:,8}))/42, (sum(jwrk_16{:,8})+sum(jscat_16{:,8}))/42]), 'FaceColor',"#6699CC","FaceAlpha",0.7);
% hold on
% % Slurm:
% bar(x,([sum(slurm_serial)/21, (sum(swrk_2{:,8})+sum(sscat_2{:,8}))/42, (sum(swrk_4{:,8})+sum(sscat_4{:,8}))/42, (sum(swrk_8{:,8})+sum(sscat_8{:,8}))/42, (sum(swrk_16{:,8})+sum(sscat_16{:,8}))/42]), 'FaceColor',"#DDCC77","FaceAlpha",0.3);
% % Dica:
% bar(x,([sum(dica_serial{:,8})/21, (sum(dwrk_2{:,8})+sum(dscat_2{:,8}))/42, (sum(dwrk_4{:,8})+sum(dscat_4{:,8}))/42, (sum(dwrk_8{:,8})+sum(dscat_8{:,8}))/42, (sum(dwrk_16{:,8})+sum(dscat_16{:,8}))/42]), 'FaceColor',"#EE99AA","FaceAlpha",0.7);
% legend(["Jaguar 1", "Slurm", "Dica 10"])
% xticklabels(["1 (Serial)", "2", "4", "8", "16"]);
% xtickangle(45);
% fontname("Times New Roman");
% xlabel('Number of Processes', "FontWeight","bold");
% ylabel('Wall Time (s)', "FontWeight","bold");
% grid on;

%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% figure(10)
% %subplot(1,3,1)
% hold on;
% boxplot(log10([wrk_2.Total_Time, wrk_4.Total_Time, wrk_8.Total_Time, wrk_16.Total_Time, serial.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(204/255) (187/255) (68/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(5),'XData'),get(h(5),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Worker Method: Total")
% %x-axis
% xticklabels(["2", "4", "8", "16", "1 (Serial)"]);
% xtickangle(45);
% xlabel('Number of Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% 
% %%%%%%%%%%%%%%
% subplot(1,3,2)
% hold on;
% boxplot(log10([wrk_2.Job_Time, wrk_4.Job_Time, wrk_8.Job_Time, wrk_16.Job_Time, serial.Job_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(204/255) (187/255) (68/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(5),'XData'),get(h(5),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Worker Method: Job")
% xticklabels(["2", "4", "8", "16", "1 (Serial)"]);
% xtickangle(45);
% xlabel('Number of Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% 
% %%%%%%%%%%%%%%
% subplot(1,3,3)
% hold on;
% boxplot(log10([wrk_2.Extract_Time, wrk_4.Extract_Time, wrk_8.Extract_Time, wrk_16.Extract_Time, serial.Extract_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(204/255) (187/255) (68/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(5),'XData'),get(h(5),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Worker Method: Extract")
% xticklabels(["2", "4", "8", "16", "1 (Serial)"]);
% xtickangle(45);
% xlabel('Number of Processes');
% ylabel('Wall Time (s)');
% grid on;

% figure (11);
% tiledlayout(1,3, "TileSpacing","compact", "Padding","compact")
% nexttile
% %subplot(1,3,1)
% hold on;
% boxplot(log10([scat_2.Total_Time, scat_4.Total_Time, scat_8.Total_Time, scat_16.Total_Time, serial.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(136/255) (34/255) (85/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(165/255) (0/255) (38/255)],'FaceAlpha',0.3);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(238/255) (119/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [(0/255) (153/255) (136/255)],'FaceAlpha',0.7);
% patch(get(h(5),'XData'),get(h(5),'YData'), [(0/255) (68/255) (136/255)],'FaceAlpha',0.7);
% 
% title("Scatter Method: Total")
% %x-axis
% xticklabels(["2", "4", "8", "16", "1 (Serial)"]);
% xtickangle(45);
% xlabel('Number of Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% 
% %%%%%%%%%%%%%%
% nexttile
% %subplot(1,3,2)
% hold on;
% boxplot(log10([scat_2.Job_Time, scat_4.Job_Time, scat_8.Job_Time, scat_16.Job_Time, serial.Job_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(136/255) (34/255) (85/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(165/255) (0/255) (38/255)],'FaceAlpha',0.3);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(238/255) (119/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [(0/255) (153/255) (136/255)],'FaceAlpha',0.7);
% patch(get(h(5),'XData'),get(h(5),'YData'), [(0/255) (68/255) (136/255)],'FaceAlpha',0.7);
% 
% title("Scatter Method: Job")
% %x-axis
% xticklabels(["2", "4", "8", "16", "1 (Serial)"]);
% xtickangle(45);
% xlabel('Number of Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% 
% %%%%%%%%%%%%%%
% nexttile;
% hold on;
% boxplot(log10([scat_2.Extract_Time, scat_4.Extract_Time, scat_8.Extract_Time, scat_16.Extract_Time, serial.Extract_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(136/255) (34/255) (85/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(165/255) (0/255) (38/255)],'FaceAlpha',0.3);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(238/255) (119/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [(0/255) (153/255) (136/255)],'FaceAlpha',0.7);
% patch(get(h(5),'XData'),get(h(5),'YData'), [(0/255) (68/255) (136/255)],'FaceAlpha',0.7);
% 
% title("Scatter Method: Extract")
% xticklabels(["2", "4", "8", "16", "1 (Serial)"]);
% xtickangle(45);
% xlabel('Number of Processes');
% ylabel('Wall Time (s)');
% grid on;

%% Variability in slurm results (OLD)
% %SLURM results:
% slurm_t1 = readtable('srun_1.csv');
% slurm_t2 = readtable('srun_2.csv');
% slurm_t3 = readtable('srun_3.csv');
% slurm_t4 = readtable('srun_4.csv');
% 
% % Grouping processing times of each document page:
% s1_serial = slurm_t1(strcmp(slurm_t1.Method,'Serial'),:);
% s1_wrks = slurm_t1(strcmp(slurm_t1.Method,'Workers'),:);
% s1_scats = slurm_t1(strcmp(slurm_t1.Method,'Scatter'),:);
% %
% s2_serial = slurm_t2(strcmp(slurm_t2.Method,'Serial'),:);
% s2_wrks = slurm_t2(strcmp(slurm_t2.Method,'Workers'),:);
% s2_scats = slurm_t2(strcmp(slurm_t2.Method,'Scatter'),:);
% %
% s3_serial = slurm_t3(strcmp(slurm_t3.Method,'Serial'),:);
% s3_wrks = slurm_t3(strcmp(slurm_t3.Method,'Workers'),:);
% s3_scats = slurm_t3(strcmp(slurm_t3.Method,'Scatter'),:);
% %
% s4_serial = slurm_t4(strcmp(slurm_t4.Method,'Serial'),:);
% s4_wrks = slurm_t4(strcmp(slurm_t4.Method,'Workers'),:);
% s4_scats = slurm_t4(strcmp(slurm_t4.Method,'Scatter'),:);
% 
% %%%%% run 1 %%%%%
% wrk_21 = s1_wrks(1:7,:);
% wrk_41 = s1_wrks(8:14,:);
% wrk_81 = s1_wrks(15:21,:);
% wrk_161 = s1_wrks(22:28,:);
% 
% scat_21 = s1_scats(1:7,:);
% scat_41 = s1_scats(8:14,:);
% scat_81 = s1_scats(15:21,:);
% scat_161 = s1_scats(22:28,:);
% 
% %%%%% run 2 %%%%%
% wrk_22 = s2_wrks(1:7,:);
% wrk_42 = s2_wrks(8:14,:);
% wrk_82 = s2_wrks(15:21,:);
% wrk_162 = s2_wrks(22:28,:);
% 
% scat_22 = s2_scats(1:7,:);
% scat_42 = s2_scats(8:14,:);
% scat_82 = s2_scats(15:21,:);
% scat_162 = s2_scats(22:28,:);
% 
% %%%%% run 3 %%%%%
% wrk_23 = s3_wrks(1:7,:);
% wrk_43 = s3_wrks(8:14,:);
% wrk_83 = s3_wrks(15:21,:);
% wrk_163 = s3_wrks(22:28,:);
% 
% scat_23 = s3_scats(1:7,:);
% scat_43 = s3_scats(8:14,:);
% scat_83 = s3_scats(15:21,:);
% scat_163 = s3_scats(22:28,:);
% 
% %%%%% run 4 %%%%%
% wrk_24 = s4_wrks(1:7,:);
% wrk_44 = s4_wrks(8:14,:);
% wrk_84 = s4_wrks(15:21,:);
% wrk_164 = s4_wrks(22:28,:);
% 
% scat_24 = s4_scats(1:7,:);
% scat_44 = s4_scats(8:14,:);
% scat_84 = s4_scats(15:21,:);
% scat_164 = s4_scats(22:28,:);

%% old old
% % Grouping processing times of each document page:
% serial = time_t(strcmp(time_t.Method,'Serial'),:);
% wrks = time_t(strcmp(time_t.Method,'Workers'),:);
% scats = time_t(strcmp(time_t.Method,'Scatter'),:);
% 
% wrk_2 = wrks(1:7,:);
% wrk_4 = wrks(8:14,:);
% wrk_8 = wrks(15:21,:);
% wrk_16 = wrks(22:28,:);
% 
% scat_2 = scats(1:7,:);
% scat_4 = scats(8:14,:);
% scat_8 = scats(15:21,:);
% scat_16 = scats(22:28,:);
% Compare Scatter to Worker
% figure(8)
% x = 1:5;
% bar(x,([sum(wrk_2{:,8})/7, sum(wrk_4{:,8})/7, sum(wrk_8{:,8})/7, sum(wrk_16{:,8})/7, sum(serial{:,8})/7]), 'FaceColor',"#009988");
% hold on
% bar(x,([sum(scat_2{:,8})/7, sum(scat_4{:,8})/7, sum(scat_8{:,8})/7, sum(scat_16{:,8})/7, sum(serial{:,8})/7]), 'FaceColor',"#EE3377","FaceAlpha",0.4);
% legend(["Workers", "Scatter"])
% xticklabels(["2", "4", "8", "16", "1 (Serial)"]);
% xtickangle(45);
% fontname("Times New Roman");
% xlabel('Number of Processes', "FontWeight","bold");
% ylabel('Wall Time (s)', "FontWeight","bold");
% grid on;
% % % % % % % % %
% x= 1:4;
% %Worker Method comparisons
% figure (12);
% tiledlayout(2,2, "TileSpacing","compact", "Padding","compact");
% fontname("Times New Roman");
% %%%%%%%%%%%%%%
% nexttile
% n = 2;
% hold on;
% boxplot(([wrk_21.Total_Time, wrk_22.Total_Time, wrk_23.Total_Time, wrk_24.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Worker Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 2 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% %%%%%%%%%%%%%%
% nexttile
% n = 4;
% hold on;
% boxplot(([wrk_41.Total_Time, wrk_42.Total_Time, wrk_43.Total_Time, wrk_44.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Worker Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 4 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% %%%%%%%%%%%%%%
% nexttile
% n = 8;
% hold on;
% boxplot(([wrk_81.Total_Time, wrk_82.Total_Time, wrk_83.Total_Time, wrk_84.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Worker Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 8 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% %%%%%%%%%%%%%%
% nexttile
% n = 16;
% hold on;
% boxplot(([wrk_161.Total_Time, wrk_162.Total_Time, wrk_163.Total_Time, wrk_164.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Worker Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 16 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% figure (13);
% tiledlayout(2,2, "TileSpacing","compact", "Padding","compact");
% fontname("Times New Roman");
% %%%%%%%%%%%%%%
% nexttile
% n = 2;
% hold on;
% boxplot(([scat_21.Total_Time, scat_22.Total_Time, scat_23.Total_Time, scat_24.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Scatter Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 2 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% %%%%%%%%%%%%%%
% nexttile
% n = 4;
% hold on;
% boxplot(([scat_41.Total_Time, scat_42.Total_Time, scat_43.Total_Time, scat_44.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Scatter Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 4 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% %%%%%%%%%%%%%%
% nexttile
% n = 8;
% hold on;
% boxplot(([scat_81.Total_Time, scat_82.Total_Time, scat_83.Total_Time, scat_84.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Scatter Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 8 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;
% %%%%%%%%%%%%%%
% nexttile
% n = 16;
% hold on;
% boxplot(([scat_161.Total_Time, scat_162.Total_Time, scat_163.Total_Time, scat_164.Total_Time]), x,"Widths", 0.8, 'Symbol','*-k');
% 
% h = findobj(gca,'Tag','Box');
% % Formatting:
% patch(get(h(1),'XData'),get(h(1),'YData'), [(140/255) (78/255) (153/255)],'FaceAlpha',0.7);
% patch(get(h(2),'XData'),get(h(2),'YData'), [(238/255) (102/255) (119/255)],'FaceAlpha',0.7);
% patch(get(h(3),'XData'),get(h(3),'YData'), [(34/255) (136/255) (51/255)],'FaceAlpha',0.7);
% patch(get(h(4),'XData'),get(h(4),'YData'), [0 (119/255) (187/255)],'FaceAlpha',0.7);
% 
% title("Scatter Method: Total")
% %x-axis
% xticklabels(["1", "2", "3", "4"]);
% xtickangle(45);
% xlabel('SLURM set (n): 16 Processes');
% %y-axis
% ylabel('Wall Time (s)');
% grid on;

%%
% Serial performance times for each document:
% %Plot the results:
% figure(14) % Serial Processing Times for Different Processes
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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% figure(15) %Log Bar Graphs: 
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
% %% Total times per doc:
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
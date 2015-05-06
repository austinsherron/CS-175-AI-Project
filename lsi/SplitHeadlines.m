f = fileread('original-data-w-articles.csv');
headlines = strsplit(f, '\n');

clusteredHeadlines = cell(length(unique(idx)), length(headlines));
clusteredHeadlinesCount = ones(length(unique(idx)), 1);
for i = 1:length(headlines)
    class = idx(i);
    clusteredHeadlines{class, clusteredHeadlinesCount(class)} = headlines{i};
    clusteredHeadlinesCount(class) = clusteredHeadlinesCount(class) + 1;
end

fid = fopen('clustered_headlines.txt', 'w');
    for i = 1:length(clusteredHeadlinesCount)
        for j = 1:clusteredHeadlinesCount(i)
            fprintf(fid, '%s\n', clusteredHeadlines{i, j});
        end
        fprintf(fid, '\n\n');
    end
fclose(fid);

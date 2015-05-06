% disp('Building X');
% X = zeros(n, k);
% for i = 1:n
%     % Compute the rank for a document by computing its 'column' and
%     % multiplying it by the transform matrix
%     X(i,:) = documentToA(keyToIndexMap, g, docs{i})' * transformMatrix;
% end
X = pts;
k = 3;

disp('Clustering');
idx = kmeans(X, k);
classes = cell(k, 1);

hold on;
colors = {'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'black', [.5 .5 .5]};
for i = 1:k
    classes{i} = X(idx == i, :);
    scatter(classes{i}(:,1), classes{i}(:,2), 'MarkerFaceColor', colors{i});
end

save 'cluster';

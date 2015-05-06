% Output vector length
k = 2;

% Path to file
filePath = 'headlines-wo-stopwords.csv';
f = fileread(filePath);

% Split by lines
scannedLines = textscan(f, '%s', 'delimiter', '\n');
lines = strtrim(scannedLines{1});
lines = lines(1:end-1);

% List of documents
docs = cell(size(lines));

% number of documents
n = length(docs);

% number of terms
scannedTokens = textscan(f, '%s', 'delimiter', ',');
m = length(unique(strtrim(scannedTokens{1})));

% Map of word to word count globally
globalWordCount = containers.Map();

% Map of word to an index
keyToIndexMap = containers.Map();

% Index
ind = 1;

% Matrix of values built according to Wikipedia
A = zeros(m, n);

% Term frequency per document
tf = zeros(m, n);

% Global term frequency
gf = zeros(m, 1);

% value used to calculate A
g = ones(m, 1);

disp('Counting');

% For each document
for i = 1:n
    % Build a document by splitting into words
    tokens = textscan(lines{i}, '%s', 'delimiter', ',');
    docs{i} = strtrim(tokens{1});
    % For each word
    for j = 1:length(docs{i})
        % Get the word
        key = docs{i}{j};
        % Add to the globalWordCount map
        addToMap(globalWordCount, key);
        % update indices if necessary
        if ~isKey(keyToIndexMap, key)
            keyToIndexMap(key) = ind;
            ind = ind + 1;
        end
        % Update the term frequency matrix
        tf(keyToIndexMap(key), i) = tf(keyToIndexMap(key), i) + 1;
    end
end

disp('Calculting heuristics');
% Calculate g for computing A
pTemp = tf ./ repmat(g, 1, n);
p = (pTemp .* log2(pTemp + 1e-100)) / log2(n);
g = g + sum(p, 2);

disp('Building document');
for i = 1:n
    % Concatenate the columns of documents for A
    A(:,i) = documentToA(keyToIndexMap, g, docs{i});
end

disp('SVD');
% Singlular value decomposition
[T, S, Dt] = svds(A, k);
% transform matrix to multiply future documents by to rank
transformMatrix = T * inv(S);

pts = zeros(n, k);
for i = 1:n
    % Compute the rank for a document by computing its 'column' and
    % multiplying it by the transform matrix
    pts(i,:) = documentToA(keyToIndexMap, g, docs{i})' * transformMatrix;
end

if k == 1
    scatter(1:length(pts), pts);
else
    scatter(pts(:,1), pts(:,2));
end

interface SearchFiltersProps {
  queries: string[];
  selectedQuery: string;
  onQueryChange: (query: string) => void;
  searchTerm: string;
  onSearchChange: (term: string) => void;
}

export function SearchFilters({
  queries,
  selectedQuery,
  onQueryChange,
  searchTerm,
  onSearchChange,
}: SearchFiltersProps) {
  return (
    <div className="flex flex-col sm:flex-row gap-4 mb-6">
      <select
        value={selectedQuery}
        onChange={(e) => onQueryChange(e.target.value)}
        className="px-4 py-2 border rounded-md bg-white text-gray-900 shadow-sm"
      >
        <option value="">All Categories</option>
        {queries.map((query) => (
          <option key={query} value={query}>
            {query}
          </option>
        ))}
      </select>

      <input
        type="text"
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
        placeholder="Search products..."
        className="px-4 py-2 border rounded-md flex-grow bg-white text-gray-900 shadow-sm placeholder-gray-500"
      />
    </div>
  );
}

"use client";

import { useState, useEffect } from "react";
import { ProductTable } from "@/components/ProductTable";
import { SearchFilters } from "@/components/SearchFilters";

// Import the Product type
type Product = {
  title: string;
  price: number | null;
  total_reviews: number | null;
  image_url: string;
  search_query: string;
  product_url: string;
  scrape_date: string;
};

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [queries, setQueries] = useState<string[]>([]);
  const [selectedQuery, setSelectedQuery] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your actual API endpoint
        const response = await fetch("/api/products");
        const data = await response.json();
        setProducts(data);
        setFilteredProducts(data);

        // Extract unique queries
        const uniqueQueries = [
          ...new Set(data.map((p: Product) => p.search_query)),
        ].filter((query): query is string => typeof query === "string");
        setQueries(uniqueQueries);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    let filtered = [...products];

    if (selectedQuery) {
      filtered = filtered.filter((p) => p.search_query === selectedQuery);
    }

    if (searchTerm) {
      filtered = filtered.filter((p) =>
        p.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredProducts(filtered);
  }, [selectedQuery, searchTerm, products]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8 max-w-[1400px] bg-white text-gray-900 shadow-sm">
      <h1 className="text-3xl font-bold mb-8 ">
        Amazon Product Scraper Results
      </h1>

      <SearchFilters
        queries={queries}
        selectedQuery={selectedQuery}
        onQueryChange={setSelectedQuery}
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
      />

      <div className="overflow-x-auto">
        <ProductTable data={filteredProducts} />
      </div>

      <div className="mt-4 text-sm text-gray-500">
        Showing {filteredProducts.length} of {products.length} products
      </div>
    </main>
  );
}

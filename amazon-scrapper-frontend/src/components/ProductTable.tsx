import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
  SortingState,
} from "@tanstack/react-table";
import { useState } from "react";
import { format } from "date-fns";

type Product = {
  title: string;
  price: number | null;
  total_reviews: number | null;
  image_url: string;
  search_query: string;
  product_url: string;
  scrape_date: string;
};

const columnHelper = createColumnHelper<Product>();

const columns = [
  columnHelper.accessor("image_url", {
    header: "Image",
    cell: (info) => (
      <img
        src={info.getValue()}
        alt={info.row.original.title}
        className="w-16 h-16 object-contain"
      />
    ),
    size: 100,
  }),
  columnHelper.accessor("title", {
    header: "Product Title",
    cell: (info) => (
      <div className="max-w-xs">
        <a
          href={info.row.original.product_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800 truncate block font-medium"
          title={info.getValue()}
        >
          {info.getValue()}
        </a>
      </div>
    ),
    size: 300,
  }),
  columnHelper.accessor("price", {
    header: "Price",
    cell: (info) => (
      <span className="font-medium">
        {info.getValue() ? `$${info.getValue()?.toFixed(2)}` : "N/A"}
      </span>
    ),
    size: 80,
  }),
  columnHelper.accessor("total_reviews", {
    header: "Reviews",
    cell: (info) => (
      <span className="font-medium">
        {info.getValue()?.toLocaleString() ?? "N/A"}
      </span>
    ),
    size: 80,
  }),
  columnHelper.accessor("search_query", {
    header: "Search Query",
    cell: (info) => (
      <div
        className="max-w-[150px] truncate text-gray-900 font-medium"
        title={info.getValue()}
      >
        {info.getValue()}
      </div>
    ),
    size: 150,
  }),
  columnHelper.accessor("scrape_date", {
    header: "Scraped On",
    cell: (info) => (
      <span className="text-gray-900 font-medium">
        {format(new Date(info.getValue()), "MMM d, yyyy")}
      </span>
    ),
    size: 120,
  }),
];

export function ProductTable({ data }: { data: Product[] }) {
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    state: {
      sorting,
    },
    onSortingChange: setSorting,
  });

  return (
    <div className="overflow-x-auto shadow-md rounded-lg bg-white">
      <table className="w-full table-auto border-collapse">
        <thead>
          <tr className="bg-gray-800 text-white">
            {table.getFlatHeaders().map((header) => (
              <th
                key={header.id}
                className="px-4 py-3 text-left text-sm font-semibold"
                style={{ width: header.getSize() }}
              >
                {flexRender(
                  header.column.columnDef.header,
                  header.getContext()
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row, index) => (
            <tr
              key={row.id}
              className={`
                border-t border-gray-200 
                hover:bg-gray-50 
                ${index % 2 === 0 ? "bg-white" : "bg-gray-50"}
              `}
            >
              {row.getVisibleCells().map((cell) => (
                <td
                  key={cell.id}
                  className="px-4 py-3 text-sm text-gray-900"
                  style={{ width: cell.column.getSize() }}
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

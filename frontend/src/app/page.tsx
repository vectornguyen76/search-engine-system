"use client"

import Image from 'next/image'
import { useState, useEffect } from 'react'
import { AiFillCamera } from "react-icons/ai";

interface DataSearchType {
  item_name: string
  item_path: string
  item_image: string
  fixed_item_price: number
  sale_item_price: number
  sale_rate: number
  sales_number: number
  shop_path: string
  shop_name: string
}

export default function Home() {
  const [searchValue, setSearchValue] = useState<string>('');
  const [dataSearch, setDataSearch] = useState<DataSearchType[]>([])
  const [loading, setLoading] = useState<boolean>(false);
  const [showUpload, setShowUpload] = useState<boolean>(false);

  const NEXT_PUBLIC_IMAGE_SEARCH = process.env.NEXT_PUBLIC_IMAGE_SEARCH!;
  const NEXT_PUBLIC_TEXT_SEARCH = process.env.NEXT_PUBLIC_TEXT_SEARCH!;

  const handleClickSearch = async () => {
    setLoading(true)
    const apiUrl = `${NEXT_PUBLIC_TEXT_SEARCH}/full-text-search?query=${searchValue}&size=20`
    fetch(apiUrl, { method: 'GET' })
      .then((response) => response.json())
      .then((data) => {
        setDataSearch(data)
        setLoading(false);
      })
      .catch((error) => {
        setLoading(true);
        console.error('Error fetching data:', error);
      });
  }

  const handleClickUpload = async () => {
    setShowUpload(!showUpload)
  }

  const handleFileUpload = async (event: any) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      console.log('Selected file:', selectedFile.name);
      setLoading(true);
      setShowUpload(false);

      const formData = new FormData();
      formData.append('file', selectedFile);

      try {
        const response = await fetch(`${NEXT_PUBLIC_IMAGE_SEARCH}/search-image`, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          // Handle the API response here
          console.log('API Response:', data);
          setDataSearch(data)
          setLoading(false);
          setShowUpload(false);
        } else {
          // Handle non-successful response (e.g., status code is not 200)
          console.error('API Error:', response.statusText);
        }
      } catch (error) {
        // Handle network or other errors
        console.error('Error:', error);
      }
    }
  };

  return (
    <>
      <div className="container mx-auto">
        {/* Search bar */}
        <div className='search m-10'>
          <div className="flex items-center justify-center">
            <div className="flex border-2 rounded">
              <input
                type="text"
                className="px-4 py-2 w-80"
                placeholder="Search..."
                onChange={(e) => setSearchValue(e.target.value)}
                onKeyUp={(e) => {
                  if (e.key === "Enter") {
                    handleClickSearch();
                  }
                }}
              />
              <button className="flex items-center justify-center px-4 border-l" value={searchValue} onClick={handleClickUpload}>
                <AiFillCamera />
              </button>
              <button className="flex items-center justify-center px-4 border-l" value={searchValue} onClick={handleClickSearch}>
                <svg className="w-6 h-6 text-gray-600" fill="currentColor" xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24">
                  <path
                    d="M16.32 14.9l5.39 5.4a1 1 0 0 1-1.42 1.4l-5.38-5.38a8 8 0 1 1 1.41-1.41zM10 16a6 6 0 1 0 0-12 6 6 0 0 0 0 12z" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {showUpload ? (
          <div className="flex items-center justify-center w-full mb-12">
            <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg
                  className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 16"
                >
                  {/* SVG path here */}
                </svg>
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
              </div>
              <input
                id="dropzone-file"
                type="file"
                className="hidden"
                onChange={handleFileUpload} // Attach the event handler here
              />
            </label>
          </div>
        ) : (<> </>)}

        {/* Data search */}
        {
          loading ? (
            <>
              <p>Loading...</p>
            </>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {dataSearch.map((result, index) => (
                <div className="relative flex flex-col overflow-hidden rounded-lg border border-gray-100 bg-white shadow-md" key={index}>
                  <a className="relative mx-3 mt-3 flex h-60 overflow-hidden rounded-xl" href={result.item_path} target="_blank">
                    <img className="object-cover" src={result.item_image} alt="product image" />
                    <span className="absolute top-0 left-0 m-2 rounded-full bg-black px-2 text-center text-sm font-medium text-white">39% OFF</span>
                  </a>
                  <div className="mt-4 px-5 pb-5">
                    <a href="#">
                      <h5 className="text-xl tracking-tight text-slate-900">{result.item_name}</h5>
                    </a>
                    <div className="mt-4 flex items-center justify-between">
                      <p>
                        <span className="text-3xl font-medium text-slate-900">{result.fixed_item_price}</span>
                      </p>
                      <p>
                        <span className="text-3xl font-bold text-slate-900">{result.sale_item_price}</span>
                      </p>
                      {/* <div className="flex items-center">
                        <svg aria-hidden="true" className="h-5 w-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                        </svg>
                        <svg aria-hidden="true" className="h-5 w-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                        </svg>
                        <svg aria-hidden="true" className="h-5 w-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                        </svg>
                        <svg aria-hidden="true" className="h-5 w-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                        </svg>
                        <svg aria-hidden="true" className="h-5 w-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                        </svg>
                        <span className="mr-2 ml-3 rounded bg-yellow-200 px-2.5 py-0.5 text-xs font-semibold">5.0</span>
                      </div> */}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )
        }
      </div>
    </>
  )
}

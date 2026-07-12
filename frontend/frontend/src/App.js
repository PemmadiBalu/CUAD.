
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import FileUploader from './components/FileUploader';
import ContractDetails from './components/ContractDetail';

function App() {
    const [contracts, setContracts] = useState([]);
    const [selectedContract, setSelectedContract] = useState(null);

    useEffect(() => {
        fetchContracts();
    }, []);

    const fetchContracts = async () => {
    try {
        const res = await axios.get("http://127.0.0.1:5000/api/contracts");
        setContracts(res.data);
    } catch (error) {
        console.error("Error fetching contracts:", error);

        if (error.response) {
            console.log("Status:", error.response.status);
            console.log("Data:", error.response.data);
        } else {
            console.log(error.message);
        }
    }
};

    return (
        <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
            {/* Header */}
            <motion.header 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }}
                className="bg-white border-b p-6 sticky top-0 z-10 shadow-sm"
            >
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <h1 className="text-2xl font-black text-blue-600 tracking-tighter">LEGAL.AI</h1>
                    <div className="text-sm font-medium text-slate-400">CUAD Pipeline Dashboard</div>
                </div>
            </motion.header>

            <main className="max-w-7xl mx-auto p-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Left Side: Upload & List */}
                <div className="lg:col-span-4 space-y-6">
                    <FileUploader onUploadSuccess={(newDoc) => {
                        setContracts([newDoc, ...contracts]);
                        setSelectedContract(newDoc);
                    }} />

                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                        <div className="p-4 bg-slate-50 border-b font-bold">Recent Documents</div>
                        <div className="max-h-[500px] overflow-y-auto">
                            {contracts.map((c) => (
                                <motion.div 
                                    key={c.contract_id}
                                    whileHover={{ backgroundColor: "#f8fafc" }}
                                    onClick={() => setSelectedContract(c)}
                                    className={`p-4 cursor-pointer border-b last:border-0 transition-colors ${selectedContract?.contract_id === c.contract_id ? 'bg-blue-50 border-r-4 border-blue-500' : ''}`}
                                >
                                    <p className="font-bold text-sm truncate">{c.filename}</p>
                                    <p className="text-xs text-slate-400">ID: {c.contract_id}</p>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Side: Details View */}
                <div className="lg:col-span-8">
                    {selectedContract ? (
                        <ContractDetails contract={selectedContract} />
                    ) : (
                        <motion.div 
                            initial={{ opacity: 0 }} 
                            animate={{ opacity: 1 }}
                            className="h-full flex flex-col items-center justify-center text-slate-400 border-4 border-dashed border-slate-200 rounded-3xl p-20 text-center"
                        >
                            <p className="text-lg">Select a contract or upload a new one to begin AI extraction.</p>
                        </motion.div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default App;
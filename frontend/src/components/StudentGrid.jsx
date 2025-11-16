import { DataGrid } from '@mui/x-data-grid';

const StudentGrid = ({ students }) => {
  const columns = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'name', headerName: 'Name', width: 130 },
    { field: 'grade', headerName: 'Grade', width: 90 },
    { field: 'busNumber', headerName: 'Bus #', width: 90 },
    {
      field: 'status',
      headerName: 'Status',
      width: 130,
      renderCell: (params) => (
        <div className={`px-2 py-1 rounded-full text-sm ${
          params.value === 'On Bus' 
            ? 'bg-green-100 text-green-800'
            : params.value === 'At School'
            ? 'bg-blue-100 text-blue-800'
            : 'bg-gray-100 text-gray-800'
        }`}>
          {params.value}
        </div>
      ),
    },
    {
      field: 'lastUpdate',
      headerName: 'Last Update',
      width: 180,
      valueGetter: (params) => 
        new Date(params.value).toLocaleString()
    }
  ];

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={students}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        disableSelectionOnClick
        className="bg-white rounded-lg shadow"
      />
    </div>
  );
};

export default StudentGrid;

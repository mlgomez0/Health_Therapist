export const formatDate = (dateString: string): string => {

    // Parse the date string
    const date = new Date(dateString);

    // Extract the components
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const year = date.getFullYear();

    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    // Format the date as dd/MM/yyyy hh:mm
    return `${day}/${month}/${year} ${hours}:${minutes}`;

}
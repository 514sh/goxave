import {LOGO_API_PK} from "./config"

const LOGO_API = "https://img.logo.dev"

export const stores = [
  {
    id: 1,
    name: "Amazon",
    url: "https://www.amazon.com",
    logo: `${LOGO_API}/amazon.com?token=${LOGO_API_PK}`
  },
  {
    id: 2,
    name: "Datablitz",
    url: "https://ecommerce.datablitz.com.ph",
    logo: `${LOGO_API}/ecommerce.datablitz.com.ph?token=${LOGO_API_PK}` 
  },
  {
    id: 3,
    name: "JBL Store PH",
    url: "https://jblstore.com.ph/",
    logo: `${LOGO_API}/jbl.com?token=${LOGO_API_PK}`
  },
  {
    id: 4,
    name: "Lazada",
    url: "https://www.lazada.com.ph/",
    logo: `${LOGO_API}/lazada.com.ph?token=${LOGO_API_PK}`
  },
];

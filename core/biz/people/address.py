import pyarrow as pa
from pydantic import Field, field_validator, model_validator, model_serializer
from core.data.domain.base import DomainObject

class UsaAddress(DomainObject):


    street: pa.string() = Field(..., min_length=1, max_length=100, description="Street name and number")
    city: pa.string() = Field(..., min_length=1, max_length=50, description="City name")
    state: pa.string() = Field(..., min_length=2, max_length=2, description="Two-letter state abbreviation")
    zip_code: pa.string() = Field(..., regex=r'^\d{5}(-\d{4})?$', description="5 or 9 digit zip code")
    country: pa.string() = Field(default="USA", description="Country name")

    @field_validator('state')
    def validate_state(cls, value):
        if value.upper() not in ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
                                 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
                                 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
                                 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']:
            raise ValueError('Invalid state abbreviation')
        return value.upper()

    @model_validator(pre=True)
    def validate_address(cls, values):
        street = values.get('street')
        city = values.get('city')
        if not street or not city:
            raise ValueError('Street and city must be provided')
        return values

    def full_address(self) -> str:
        """Returns the full address as a single string."""
        address_parts = [self.street, self.city, self.state, self.zip_code, self.country]
        return ', '.join(part for part in address_parts if part)


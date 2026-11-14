# VAHAN 2025 | Evidence behind the findings

## October's jump appears in a separate published report

| Series | September 2025 | October 2025 | Month-over-month change |
| --- | ---: | ---: | ---: |
| Project's VAHAN exports | 1,931,085 | 4,170,511 | +116.0% |
| FADA's published vehicle retail series | 1,827,337 | 4,023,923 | +120.21% |

Both series more than doubled. FADA is a separate publication drawing on registration data, so this corroborates the direction and scale of the jump rather than independently reproducing the project totals. Coverage and reporting snapshots should be aligned before using the totals interchangeably.

Within FADA's series, two-wheelers went from 1,287,735 to 3,149,846. That is **1,862,111 of the 2,196,586 net additional vehicles (84.8%)**. This is evidence that the surge was concentrated in two-wheelers in FADA's series. It does not identify the vehicle class of each registration in the project's maker-by-fuel exports. FADA discusses festive demand and GST changes as context; this comparison does not estimate their separate effects.

Source: [FADA October 2025 vehicle retail release, page 5](https://fada.in/images/press-release/1690d68d7a2e6cFADA%20releases%20October%202025%20%26%2042-Days%20Festive%20Vehicle%20Retail%20Data.pdf).

## The fuel result depends on the comparison window

- **September to October:** PETROL and PETROL(E20) increased from **71.91% to 81.04%** of recorded registrations together, a gain of **9.13 percentage points**. They accounted for **88.9%** of the net increase in counts.
- **January to December:** PETROL fell from **69.62% to 24.43%** and PETROL(E20) rose from **2.53% to 45.03%**, but their combined share moved only from **72.15% to 69.46%**, down **2.69 percentage points**. The large change was in the split between the reported labels. The data does not establish changes in individual buyers' fuel choices or explain why the labels shifted.

## Different manufacturers led the two fuel increases

| Reported fuel label | Largest October contributors | Combined share of the label's net increase |
| --- | --- | ---: |
| PETROL | Hero MotoCorp (+653,831) and Honda Motorcycle and Scooter India (+444,950) | 84.3% |
| PETROL(E20) | TVS Motor (+298,873) and Bajaj Auto (+169,101) | 68.1% |

These are counts within the specified fuel labels. They should not be added to the separate all-fuel manufacturer contributions in the README.

To reproduce the project figures from the [prepared data](../vahan_2025_working.csv.gz), sum registrations by month and fuel, then divide the combined counts for the two exact labels by that month's total. For manufacturer contributions, sum registrations by month, manufacturer and fuel, subtract September from October for each manufacturer and label, then rank the signed changes. The contribution percentages divide the named manufacturers' combined changes by the net change for their fuel label.

## Best next check

Compare equivalent weeks around Diwali in 2024 and 2025, then break the results down by vehicle class and state using consistent filters. That would help distinguish a recurring festive pattern from a change concentrated in particular segments or regions. A separate comparison across groups with different GST exposure would be needed to estimate a policy effect.

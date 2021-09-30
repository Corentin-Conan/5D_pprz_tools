package telemetry_client

import (
    "context"
    "errors"
    "time"

    "github.com/airmap/interfaces/src/go/ids"
    "github.com/airmap/interfaces/src/go/measurements"
    "github.com/airmap/interfaces/src/go/telemetry"
    "github.com/airmap/interfaces/src/go/tracking"
    gunits "github.com/airmap/interfaces/src/go/units"
    "github.com/golang/protobuf/ptypes"

    md "google.golang.org/grpc/metadata"
)

// Runner models run of the telemetry simulation
type Runner struct {
    config Configuration
}

// Configuration wraps all configurable parameters
type Configuration struct {
    Client telemetry.CollectorClient
}

var (
    // SourceID identifies the source of traffic
    SourceID       = "simulation"
    authToken      = "test_token"
    headerMetadata = map[string]string{
        "Authorization": "Bearer " + authToken,
    }
)

// NewRunner creates a new simulation runner
func NewRunner(config Configuration) *Runner {
    return &Runner{config}
}

// Run runs a telemetry simulator
func (r *Runner) Run(ctx context.Context) error {
    var (
        reportTicker    = time.NewTicker(time.Second * 5)
        errCh           = make(chan error)
        sysReportTicker = time.NewTicker(time.Second * 10)
        newContext      = md.NewOutgoingContext(ctx, md.New(headerMetadata))
        identities      = []*tracking.Identity{
            {
                Details: &tracking.Identity_Imei{
                    Imei: &tracking.Identity_IMEI{
                        AsString: "fake_IMEI",
                    },
                },
            },
            {
                Details: &tracking.Identity_Operation_{
                    Operation: &tracking.Identity_Operation{
                        OperationId: &ids.Operation{
                            AsString: "fake_operation_id",
                        },
                        ServiceProviderId: &ids.USS{
                            AsString: "AIRMAP",
                        },
                    },
                },
            },
        }
    )

    stream, err := r.config.Client.ConnectProvider(newContext)
    if err != nil {
        return err
    }

    go func() {
        for {
            if _, err := stream.Recv(); err != nil {
                errCh <- err
                return
            }

            select {
            case <-newContext.Done():
                errCh <- newContext.Err()
                return
            default:
                // empty on purpose
            }
        }
    }()

    for {
        select {
        case _, ok := <-reportTicker.C:
            if !ok {
                return errors.New("failed to read from ticker channel")
            }

            rep := &telemetry.Report{
                Observed: ptypes.TimestampNow(),
                Details: &telemetry.Report_Spatial_{
                    Spatial: &telemetry.Report_Spatial{
                        Position: &measurements.Position{
                            Details: &measurements.Position_Absolute_{
                                Absolute: &measurements.Position_Absolute{
                                    Coordinate: &measurements.Coordinate2D{
                                        Longitude: &gunits.Degrees{
                                            Value: 180,
                                        },
                                        Latitude: &gunits.Degrees{
                                            Value: 180,
                                        },
                                    },
                                    Altitude: &measurements.Altitude{
                                        Height: &gunits.Meters{
                                            Value: 100,
                                        },
                                        Reference: measurements.Altitude_REFERENCE_ELLIPSOID,
                                    },
                                },
                            },
                        },
                        Velocity: &measurements.Velocity{
                            Details: &measurements.Velocity_Polar_{
                                Polar: &measurements.Velocity_Polar{
                                    Heading: &gunits.Degrees{
                                        Value: 60,
                                    },
                                    GroundSpeed: &gunits.MetersPerSecond{
                                        Value: 40,
                                    },
                                },
                            },
                        },
                    },
                },
            }
            rep.Identities = identities

            u := &telemetry.Update_FromProvider{
                Details: &telemetry.Update_FromProvider_Report{
                    Report: rep,
                },
            }

            if err := stream.Send(u); err != nil {
                return err
            }
        case _, ok := <-sysReportTicker.C:
            if !ok {
                return errors.New("failed to read from second ticket channel")
            }

            // r := &telemetry.Report{
            //     Observed: ptypes.TimestampNow(),
            //     Details: &telemetry.Report_System_{
            //         System: &telemetry.Report_System{
            //             Endurance: ptypes.DurationProto(time.Minute * 30),
            //         },
            //     },
            // }
            // r.Identities = identities

            // if err := stream.Send(&telemetry.Update_FromProvider{
            //     Details: &telemetry.Update_FromProvider_Report{
            //         Report: r,
            //     },
            // }); err != nil {
            //     return err
            // }
        case <-newContext.Done():
            return nil
        case err = <-errCh:
            return err
        }
    }
}
